# -*- coding: utf-8 -*-
"""
Category forms
"""
from django import forms
from django.template.defaultfilters import slugify

from forum.forms import CrispyFormMixin

from forum.models import Category, Thread

class CategoryForm(CrispyFormMixin, forms.ModelForm):
    """
    Category form
    """
    crispy_form_helper_path = 'forum.forms.layouts.category_helper'
    
    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        super(forms.ModelForm, self).__init__(*args, **kwargs)
    
    class Meta:
        model = Category
