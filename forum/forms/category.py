# -*- coding: utf-8 -*-
"""
Category forms
"""
from django import forms
from django.template.defaultfilters import slugify

from forum.forms import CrispyFormMixin

from forum.models import Category, Thread

class CategoryCreateForm(CrispyFormMixin, forms.ModelForm):
    """
    Formulaire de création
    """
    def __init__(self, *args, **kwargs):
        super(CategoryCreateForm, self).__init__(*args, **kwargs)
        super(forms.ModelForm, self).__init__(*args, **kwargs)
    
    def save(self):
        category_instance = Category.objects.create(
            slug=slugify(self.cleaned_data["title"]),
            order=self.cleaned_data["order"],
            title=self.cleaned_data["title"],
            description=self.cleaned_data["description"],
            visible=self.cleaned_data["visible"]
        )
        
        return category_instance
    
    class Meta:
        model = Category
        exclude = ('slug',)

class CategoryEditForm(CrispyFormMixin, forms.ModelForm):
    """
    Formulaire d'édition
    """
    def __init__(self, *args, **kwargs):
        super(CategoryEditForm, self).__init__(*args, **kwargs)
        super(forms.ModelForm, self).__init__(*args, **kwargs)
    
    def save(self):
        self.instance.slug = self.cleaned_data["slug"]
        self.instance.order = self.cleaned_data["order"]
        self.instance.title = self.cleaned_data["title"]
        self.instance.description = self.cleaned_data["description"]
        self.instance.visible = self.cleaned_data["visible"]
        self.instance.save()
        
        return self.instance
    
    class Meta:
        model = Category
        exclude = ()
