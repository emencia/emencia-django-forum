# -*- coding: utf-8 -*-
"""
Category forms
"""
from django.conf import settings
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

from forum.forms import CrispyFormMixin
from forum.utils.imports import safe_import_module
from forum.models import Category, Thread

class CategoryForm(CrispyFormMixin, forms.ModelForm):
    """
    Category form
    """
    crispy_form_helper_path = 'forum.forms.crispies.category_helper'
    
    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        
        # Set the form field for Category.description
        field_helper = safe_import_module(settings.FORUM_TEXT_FIELD_HELPER_PATH)
        if field_helper is not None:
            self.fields['description'] = field_helper(self, **{'label':_('description'), 'required':True})

    def clean_description(self):
        """
        Text content validation
        """
        description = self.cleaned_data.get("description")
        validation_helper = safe_import_module(settings.FORUM_TEXT_VALIDATOR_HELPER_PATH)
        if validation_helper is not None:
            return validation_helper(self, description)
        else:
            return description
    
    class Meta:
        model = Category
