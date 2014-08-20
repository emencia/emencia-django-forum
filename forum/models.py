# -*- coding: utf-8 -*-
import math

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
import django.dispatch
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now as tz_now

from forum.forms import get_form_helper

class Category(models.Model):
    """
    Category
    """
    created = models.DateTimeField(_("created"), auto_now_add=True)
    slug = models.SlugField(_('slug'), unique=True, max_length=50)
    order = models.SmallIntegerField(_('order'))
    title = models.CharField(_("title"), blank=False, max_length=255, unique=True)
    description = models.TextField(_("description"), blank=True)
    visible = models.BooleanField(_('visible'), default=True, help_text=_("Unvisible category won't be visible nor its threads."))

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('forum:category-details', [self.slug])

    def get_last_thread(self):
        """
        Return the last modified thread 
        """
        cache_key = '_get_last_thread_cache'
        if not hasattr(self, cache_key):
            item = None
            res = self.thread_set.filter(visible=True).order_by('-modified')[0:1]
            if len(res)>0:
                item = res[0]
            setattr(self, cache_key, item)
        return getattr(self, cache_key)
    
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        permissions = (
            ('moderate', 'Moderate category'),
        )


class Thread(models.Model):
    """
    Thread
    """
    created = models.DateTimeField(_("created"), editable=False, null=True, blank=True)
    modified = models.DateTimeField(_("modified"), editable=False, null=True, blank=True, help_text=_("This only filled when a message is added."))
    author = models.ForeignKey(User, verbose_name=_("author"), editable=False, blank=False)
    category = models.ForeignKey(Category, verbose_name=_("category"))
    subject = models.CharField(_("subject"), max_length=150)
    closed = models.BooleanField(_("closed"), default=False)
    sticky = models.BooleanField(_("sticky"), default=False, help_text=_("Sticky thread will be on top of thread list."))
    announce = models.BooleanField(_("announce"), default=False, help_text=_("Announce thread can be displayed out of the forum"))
    visible = models.BooleanField(_('visible'), default=True, help_text=_("Unvisible category won't be visible nor its messages."))

    def __unicode__(self):
        return self.subject

    @models.permalink
    def get_absolute_url(self):
        return ('forum:thread-details', [self.category.slug, self.id])

    def get_first_post(self):
        """
        Retourne le premier post en date, celui créé lors de la création du fil
        """
        cache_key = '_get_starter_cache'
        if not hasattr(self, cache_key):
            item = None
            res = self.post_set.all().order_by('created')[0:1]
            if len(res)>0:
                item = res[0]
            setattr(self, cache_key, item)
        return getattr(self, cache_key)

    def get_last_post(self):
        """
        Retourne le dernier post en date
        """
        cache_key = '_get_last_poster_cache'
        if not hasattr(self, cache_key):
            item = None
            res = self.post_set.all().order_by('-created')[0:1]
            if len(res)>0:
                item = res[0]
            setattr(self, cache_key, item)
        return getattr(self, cache_key)
    
    def save(self, *args, **kwargs):
        """
        Fill 'created' and 'modified' attributes on first create
        """
        if self.created is None:
            self.created = tz_now()
        
        if self.modified is None:
            self.modified = self.created
            
        super(Thread, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = _("Thread")
        verbose_name_plural = _("Threads")
        permissions = (
            ('moderate', 'Moderate thread'),
        )


class ThreadWatch(models.Model):
    """
    Thread watch
    """
    owner = models.ForeignKey(User, verbose_name=_("owner"), blank=False)
    thread = models.ForeignKey(Thread, verbose_name=_("thread"), blank=False)

    def __unicode__(self):
        return _("Thread watch : {0}").format(self.thread.subject)
    
    class Meta:
        verbose_name = _("Thread watch")
        verbose_name_plural = _("Thread watchs")


class Post(models.Model):
    """
    Thread message
    """
    author = models.ForeignKey(User, verbose_name=_("author"), editable=False, blank=False)
    thread = models.ForeignKey(Thread, verbose_name=_("thread"))
    created = models.DateTimeField(_("created"), editable=False, blank=True, null=True)
    modified = models.DateTimeField(_("modified"), editable=False, blank=True, null=True)
    text = models.TextField(_('message'))

    def __unicode__(self):
        return _("{0}: message #{1}").format(self.thread.subject, self.id)

    def get_absolute_url(self):
        return u"{0}{1}".format(self.thread.get_absolute_url(), self.get_paginated_urlargs())
    
    def get_paginated_urlargs(self):
        """
        Return url arguments to retrieve the Post in a paginated list
        """
        position = self.get_paginated_position()
        
        if not position:
            return '#forum-post-{0}'.format(self.id)
        
        return '?page={0}#forum-post-{1}'.format(position, self.id)
    
    def get_paginated_position(self):
        """
        Return the Post position in the paginated list
        """
        # If Post list is not paginated
        if not settings.FORUM_THREAD_DETAIL_PAGINATE:
            return 0
        
        count = Post.objects.filter(thread=self.thread_id, created__lt=self.created).count() + 1
        
        return int(math.ceil(count / float(settings.FORUM_THREAD_DETAIL_PAGINATE)))
    
    def save(self, *args, **kwargs):
        """
        Fill 'created' and 'modified' attributes on first create and allways update 
        the thread's 'modified' attribute
        """
        edited = not(self.created is None)
        
        if self.created is None:
            self.created = tz_now()
        
        # Update de la date de modif. du message
        if self.modified is None:
            self.modified = self.created
        else:
            self.modified = tz_now()
        
        super(Post, self).save(*args, **kwargs)
        
        # Update de la date de modif. du thread lors de la création du message
        if not edited:
            self.thread.modified = self.created
            self.thread.save()

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")


# Declaring signals
new_message_posted_signal = django.dispatch.Signal(providing_args=["post_instance","threadwatchs"])

# Trying to import signal receiver callable
message_post_receiver = get_form_helper(settings.FORUM_NEW_POST_SIGNAL)

# Connecting signal to the receiver if any
if message_post_receiver:
    new_message_posted_signal.connect(message_post_receiver, dispatch_uid="forum.post.new_post_watcher")
