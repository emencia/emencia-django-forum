# -*- coding: utf-8 -*-
"""
Message post forms
"""
from django.conf import settings
from django import forms
from django.utils.translation import ugettext_lazy as _
import django.dispatch

from forum.forms import CrispyFormMixin
from forum.utils.imports import safe_import_module
from forum.models import new_message_posted_signal, Category, Post

class PostCreateForm(CrispyFormMixin, forms.ModelForm):
    """
    Message post create form
    """
    crispy_form_helper_path = 'forum.forms.crispies.post_helper'
    
    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop("user", None)
        self.thread_instance = kwargs.pop("thread", None)
        
        super(PostCreateForm, self).__init__(*args, **kwargs)
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        
        # Set the form field for Post.text
        field_helper = safe_import_module(settings.FORUM_TEXT_FIELD_HELPER_PATH)
        if field_helper is not None:
            self.fields['text'] = field_helper(self, **{'label':_('message'), 'required':True})
        
        # Add threadwatch checkbox
        self.fields['threadwatch'] = forms.BooleanField(label=_("Watch this thread"), initial=settings.FORUM_DEFAULT_THREADWATCH_CHECKBOX, required=False, help_text=_("You will receive an email notification for each new post in this thread. You can disable it in the thread detail if needed."))

    def clean_text(self):
        """
        Text content validation
        """
        text = self.cleaned_data.get("text")
        validation_helper = safe_import_module(settings.FORUM_TEXT_VALIDATOR_HELPER_PATH)
        if validation_helper is not None:
            return validation_helper(self, text)
        else:
            return text
    
    def clean(self):
        cleaned_data = super(PostCreateForm, self).clean()
        if not self.author.is_staff and self.thread_instance.closed:
            raise forms.ValidationError(_("This thread is closed, you can't add it a new post."))

        return cleaned_data
    
    def save(self):
        post_instance = self.thread_instance.post_set.create(
            author=self.author,
            text=self.cleaned_data["text"],
        )
        
        # Save thread watch option
        if self.cleaned_data.get("threadwatch", False) and self.thread_instance.threadwatch_set.filter(owner=self.author).count()==0:
            threadwatch_instance = self.thread_instance.threadwatch_set.create(owner=self.author)
        
        # Find threadwatchs that are not for the message owner (it don't have to notified)
        threadwatchs = self.thread_instance.threadwatch_set.all().exclude(owner=self.author)
        if threadwatchs>0:
            # Sending signal
            new_message_posted_signal.send(sender=self, post_instance=post_instance, threadwatchs=threadwatchs)
        
        return post_instance
    
    class Meta:
        model = Post
        exclude = ('thread','author')

class PostEditForm(CrispyFormMixin, forms.ModelForm):
    """
    Message post edit form
    """
    crispy_form_helper_path = 'forum.forms.crispies.post_edit_helper'
    
    def __init__(self, *args, **kwargs):
        super(PostEditForm, self).__init__(*args, **kwargs)
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        
        # Set the form field for Post.text
        field_helper = safe_import_module(settings.FORUM_TEXT_FIELD_HELPER_PATH)
        if field_helper is not None:
            self.fields['text'] = field_helper(self, **{'label':_('message'), 'required':True})

    def clean_text(self):
        """
        Text content validation
        """
        text = self.cleaned_data.get("text")
        validation_helper = safe_import_module(settings.FORUM_TEXT_VALIDATOR_HELPER_PATH)
        if validation_helper is not None:
            return validation_helper(self, text)
        else:
            return text
        
    def save(self):
        self.instance = super(PostEditForm, self).save()
        
        return self.instance
    
    class Meta:
        model = Post
        exclude = ('thread','author')

class PostDeleteForm(CrispyFormMixin, forms.ModelForm):
    """
    Message delete form
    """
    crispy_form_helper_path = 'forum.forms.crispies.post_delete_helper'
    
    confirm = forms.BooleanField(label=_("Confirm"), initial=False, required=True)
    
    def __init__(self, *args, **kwargs):
        super(PostDeleteForm, self).__init__(*args, **kwargs)
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        
    def save(self):
        thread_instance = self.instance.thread
        
        self.instance.delete()
        
        return thread_instance
    
    class Meta:
        model = Post
        exclude = ('thread','author','text')
