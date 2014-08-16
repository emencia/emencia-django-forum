# -*- coding: utf-8 -*-
"""
Thread views
"""
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views import generic
from django.views.generic.edit import FormMixin

from guardian.mixins import PermissionRequiredMixin

from braces.views import LoginRequiredMixin, UserFormKwargsMixin

from forum.utils.views import SimpleListView, ListAppendView
from forum.mixins import ModeratorRequiredMixin, ThreadQuerysetFiltersMixin
from forum.models import Category, Thread, Post

from forum.forms.post import PostCreateForm
from forum.forms.thread import ThreadCreateForm, ThreadEditForm


class LastThreadViews(LoginRequiredMixin, ThreadQuerysetFiltersMixin, SimpleListView):
    """
    Last modified thread view
    """
    template_name = 'forum/last_threads.html'
    queryset = Thread.objects.all()
    paginate_by = settings.FORUM_LAST_THREAD_PAGINATE


class ThreadDetailsView(LoginRequiredMixin, UserFormKwargsMixin, ListAppendView):
    """
    Thread list view with a form to post a new message
    """
    model = Post
    form_class = PostCreateForm
    template_name = 'forum/thread_details.html'
    paginate_by = settings.FORUM_THREAD_DETAIL_PAGINATE
    context_object_name = 'object_list'
    
    def get_queryset(self, *args, **kwargs):
        self.category_instance = get_object_or_404(Category, slug=self.kwargs['category_slug'], visible=True)
        self.thread_instance = get_object_or_404(Thread, category=self.category_instance, pk=self.kwargs['thread_id'], visible=True)
        self.queryset = self.thread_instance.post_set.select_related().order_by('created')
        
        # Mark the form as locked for non-admin users on a closed thread
        # TODO: Unlock this also for moderators
        if not self.request.user.is_staff:
            self.locked_form = self.thread_instance.closed
        
        return super(ThreadDetailsView, self).get_queryset(*args, **kwargs)
        
    def get_context_data(self, **kwargs):
        context = super(ThreadDetailsView, self).get_context_data(**kwargs)
        context.update({
            'FORUM_OWNER_MESSAGE_CAN_EDIT': settings.FORUM_OWNER_MESSAGE_CAN_EDIT,
            'category_instance': self.category_instance,
            'thread_instance': self.thread_instance,
        })
        return context

    def get_form_kwargs(self):
        kwargs = super(ThreadDetailsView, self).get_form_kwargs()
        kwargs.update({'thread': self.thread_instance})
        return kwargs

    def get_success_url(self):
        return self.object.get_absolute_url()
    
    def get(self, *args, **kwargs):
        resp = super(ThreadDetailsView, self).get(*args, **kwargs)
        
        # Choix de suivi d'un fil
        watched = (self.thread_instance.threadwatch_set.filter(owner=self.request.user).count() > 0)
        if "watch" in self.request.GET and not watched:
            threadwatch_instance = self.thread_instance.threadwatch_set.create(owner=self.request.user)
            watched = True
        elif "unwatch" in self.request.GET and watched:
            threadwatch_instance = self.thread_instance.threadwatch_set.get(owner=self.request.user)
            threadwatch_instance.delete()
            watched = False
        # Push flag in request user object
        self.request.user.watcher = watched
        
        return resp


class ThreadCreateView(LoginRequiredMixin, UserFormKwargsMixin, generic.CreateView):
    """
    Thread create view is available for anyone
    """
    model = Thread
    form_class = ThreadCreateForm
    template_name = 'forum/thread_form.html'
    #permission_required = 'forum.add_category'
    raise_exception = True
    
    def get_category(self):
        return get_object_or_404(Category, slug=self.kwargs['category_slug'], visible=True)
    
    def get(self, *args, **kwargs):
        self.category_instance = self.get_category()
        return super(ThreadCreateView, self).get(*args, **kwargs)
    
    def post(self, *args, **kwargs):
        self.category_instance = self.get_category()
        return super(ThreadCreateView, self).post(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(ThreadCreateView, self).get_context_data(**kwargs)
        context.update({
            'category_instance': self.category_instance,
        })
        return context

    def form_valid(self, form):
        form.category_instance = self.category_instance
        return super(ThreadCreateView, self).form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class ThreadEditView(LoginRequiredMixin, ModeratorRequiredMixin, UserFormKwargsMixin, generic.UpdateView):
    """
    Thread edit view
    
    Restricted to moderators
    """
    model = Thread
    form_class = ThreadEditForm
    template_name = 'forum/thread_form.html'
    context_object_name = "thread_instance"
    raise_exception = True
    
    def get_object(self, *args, **kwargs):
        return get_object_or_404(Thread, category__slug=self.kwargs['category_slug'], pk=self.kwargs['thread_id'])
        
    def get_context_data(self, **kwargs):
        context = super(ThreadEditView, self).get_context_data(**kwargs)
        context.update({
            'category_instance': self.object.category,
        })
        return context

    def check_permissions(self, request):
        """
        Check if user have global or per object moderator permissions, first on category instance, 
        if not then on thread instance
        """
        thread_instance = self.get_object()
        return self.check_moderator_permissions(request, thread_instance.category, thread_instance)

    def get_success_url(self):
        if self.object.visible:
            return self.object.get_absolute_url()
        else:
            return reverse('gestus:category-details', args=(self.object.category.slug,))
