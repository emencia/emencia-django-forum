# -*- coding: utf-8 -*-
"""
Thread forms
"""
from django.conf import settings
from django import forms
from django.utils.translation import ugettext_lazy as _

from forum.forms import CrispyFormMixin
from forum.utils.imports import safe_import_module
from forum.models import Thread

class ThreadCreateForm(CrispyFormMixin, forms.ModelForm):
    """
    Thread's create form
    """
    crispy_form_helper_path = 'forum.forms.crispies.thread_helper'
    crispy_form_helper_kwargs = {}
    
    text = forms.CharField(label=_('Message'), required=True, widget=forms.Textarea(attrs={'cols':'50'}))
    threadwatch = forms.BooleanField(label=_("Watch this thread"), initial=settings.FORUM_DEFAULT_THREADWATCH_CHECKBOX, required=False, help_text=_("You will receive an email notification for each new post in this thread. You can disable it in the thread detail if needed."))
    
    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop("user", None)
        self.form_for_moderator = kwargs.pop("for_moderator", False)
        
        # Hide some managers only fields from the crispy layout
        self.crispy_form_helper_kwargs['for_moderator'] = self.form_for_moderator
        
        super(ThreadCreateForm, self).__init__(*args, **kwargs)
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        
        # Set the form field for Post.text
        field_helper = safe_import_module(settings.FORUM_TEXT_FIELD_HELPER_PATH)
        if field_helper is not None:
            self.fields['text'] = field_helper(self, **{'label':_('message'), 'required':True})
        
        # Remove some managers only fields from the form
        if not self.form_for_moderator:
            for k in ('closed','sticky','announce','visible'):
                del self.fields[k]

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
        # Crée le nouveau fil
        thread_instance = self.category_instance.thread_set.create(
            author=self.author,
            subject=self.cleaned_data["subject"],
            closed=self.cleaned_data.get("closed", False),
            sticky=self.cleaned_data.get("sticky", False),
            announce=self.cleaned_data.get("announce", False),
            visible=self.cleaned_data.get("visible", True),
        )
        # Injecte son premier message
        post_instance = thread_instance.post_set.create(
            author=self.author,
            text=self.cleaned_data["text"],
        )
        
        if self.cleaned_data.get("threadwatch", False):
            threadwatch_instance = thread_instance.threadwatch_set.create(owner=self.author)
        
        return thread_instance
    
    class Meta:
        model = Thread
        exclude = ('category', 'author')

class ThreadEditForm(ThreadCreateForm):
    """
    Thread's edit form
    """
    crispy_form_helper_kwargs = {
        'edit_mode': True,
    }
    
    def __init__(self, *args, **kwargs):
        super(ThreadEditForm, self).__init__(*args, **kwargs)
        
        del self.fields['text']
        del self.fields['threadwatch']
    
    def save(self):
        self.instance.subject = self.cleaned_data["subject"]
        self.instance.category = self.cleaned_data["category"]
        self.instance.closed = self.cleaned_data.get("closed", False)
        self.instance.sticky = self.cleaned_data.get("sticky", False)
        self.instance.announce = self.cleaned_data.get("announce", False)
        self.instance.visible = self.cleaned_data.get("visible", True)
        self.instance.save()
        
        return self.instance
    
    class Meta:
        model = Thread
        exclude = ('author',)
