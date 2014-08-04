# -*- coding: utf-8 -*-
"""
Thread forms
"""
from django import forms

from forum.forms import CrispyFormMixin

from forum.models import Thread
from forum.forms.post import PostCreateForm

class ThreadCreateForm(CrispyFormMixin, forms.ModelForm):
    """
    Formulaire de création
    """
    text = forms.CharField(label=u'Message', required=True, widget=forms.Textarea(attrs={'cols':'50'}))
    threadwatch = forms.BooleanField(label=u"Suivre le fil", initial=True, required=False, help_text=u"Une notification sur votre email vous sera envoyée à chaque nouveau message sur ce fil. Vous conserverez la possibilité de ne plus suivre ce fil à tout moment.")
    
    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop("user", None)
        
        super(ThreadCreateForm, self).__init__(*args, **kwargs)
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        
        postform = PostCreateForm()
        #self.fields['attachment_title'] = postform.fields['attachment_title']
        #self.fields['attachment_file'] = postform.fields['attachment_file']
        
        # Vire les champs manipulables uniquement par les admins
        for k in ('closed','sticky','announce','visible'):
            if not self.author.is_staff:
                del self.fields[k]
    
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
            #attachment_file=self.cleaned_data["attachment_file"],
            #attachment_title=self.cleaned_data["attachment_title"],
        )
        
        if self.cleaned_data.get("threadwatch", False):
            threadwatch_instance = thread_instance.threadwatch_set.create(owner=self.author)
        
        return thread_instance
    
    class Meta:
        model = Thread
        exclude = ('category','author')

class ThreadEditForm(ThreadCreateForm):
    """
    Formulaire d'édition
    """
    def __init__(self, *args, **kwargs):
        super(ThreadEditForm, self).__init__(*args, **kwargs)
        
        del self.fields['text']
        #del self.fields['attachment_title']
        #del self.fields['attachment_file']
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
        exclude = ()