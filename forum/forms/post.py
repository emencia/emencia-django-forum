# -*- coding: utf-8 -*-
"""
Message post forms
"""
from django import forms

from forum.forms import CrispyFormMixin

from forum.models import Category, Post

class PostCreateForm(CrispyFormMixin, forms.ModelForm):
    """
    Message post create form
    """
    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop("user", None)
        self.thread_instance = kwargs.pop("thread", None)
        
        super(PostCreateForm, self).__init__(*args, **kwargs)
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        
        self.fields['threadwatch'] = forms.BooleanField(label=u"Suivre le fil", initial=True, required=False, help_text=u"Une notification sur votre email vous sera envoyée à chaque nouveau message sur ce fil. Vous conserverez la possibilité de ne plus suivre ce fil à tout moment.")
    
    def clean(self):
        cleaned_data = super(PostCreateForm, self).clean()
        if not self.author.is_staff and self.thread_instance.closed:
            raise forms.ValidationError("Ce fil de discussion est fermé, vous ne pouvez y ajouter de nouveaux messages.")

        return cleaned_data
    
    def save(self):
        # Crée le nouveau message
        post_instance = self.thread_instance.post_set.create(
            author=self.author,
            text=self.cleaned_data["text"],
            #attachment_file=self.cleaned_data["attachment_file"],
            #attachment_title=self.cleaned_data["attachment_title"],
        )
        # Choix de surveillance du fil par l'auteur
        if self.cleaned_data.get("threadwatch", False) and self.thread_instance.threadwatch_set.filter(owner=self.author).count()==0:
            threadwatch_instance = self.thread_instance.threadwatch_set.create(owner=self.author)
        
        threadwatchs = self.thread_instance.threadwatch_set.all().exclude(owner=self.author)
        if threadwatchs>0:
            # TODO: Redo the sending mail process
            #MailControler = mailings_site.get_controler('forum_notify_new_post')
            #MailControler.set_context(extra_context={
                #'thread_instance': self.thread_instance,
                #'post_instance': post_instance,
            #})
            #MailControler.send_separate_mail([item.owner for item in threadwatchs])
            pass
        
        
        return post_instance
    
    class Meta:
        model = Post
        exclude = ('thread','author')

class PostEditForm(CrispyFormMixin, forms.ModelForm):
    """
    Message post edit form
    """
    def __init__(self, *args, **kwargs):
        super(PostEditForm, self).__init__(*args, **kwargs)
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        
    def save(self):
        self.instance = super(PostEditForm, self).save()
        
        return self.instance
    
    class Meta:
        model = Post
        exclude = ('thread','author')
