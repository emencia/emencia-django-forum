# -*- coding: utf-8 -*-
"""
Category forms
"""
from django import forms
from django.template.defaultfilters import slugify

from rstview.parser import SourceReporter, map_parsing_errors

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

    def clean_description(self):
        """
        Parse le contenu pour vérifier qu'il ne contient par d'erreurs de syntaxe
        """
        content = self.cleaned_data.get("description")
        if content:
            errors = SourceReporter(content)
            if errors:
                raise forms.ValidationError(map(map_parsing_errors, errors))
        return content
    
    class Meta:
        model = Category
