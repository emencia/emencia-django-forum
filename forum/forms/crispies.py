"""
Crispy forms layouts
"""
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms_foundation.layout import Layout, Row, Column, ButtonHolderPanel, Submit

def category_helper(form_tag=True):
    """
    Category's form layout helper
    """
    helper = FormHelper()
    helper.form_action = '.'
    helper.attrs = {'data_abide': ''}
    helper.form_tag = form_tag
    
    helper.layout = Layout(
        Row(
            Column(
                'title',
                css_class='small-12'
            ),
        ),
        Row(
            Column(
                'slug',
                css_class='small-12 medium-10'
            ),
            Column(
                'order',
                css_class='small-12 medium-2'
            ),
        ),
        Row(
            Column(
                'description',
                css_class='small-12'
            ),
        ),
        Row(
            Column(
                'visible',
                css_class='small-12'
            ),
        ),
        ButtonHolderPanel(
            Submit('submit', _('Submit')),
            css_class='text-right',
        ),
    )
    
    return helper



def thread_helper(form_tag=True, edit_mode=False):
    """
    Thread's form layout helper
    """
    helper = FormHelper()
    helper.form_action = '.'
    helper.attrs = {'data_abide': ''}
    helper.form_tag = form_tag
    
    fieldsets = [
        Row(
            Column(
                'subject',
                css_class='small-12'
            ),
        ),
    ]
    
    # Category field only in edit form
    if edit_mode:
        fieldsets.append(
            Row(
                Column(
                    'category',
                    css_class='small-12'
                ),
            ),
        )
    
    fieldsets.append(
        Row(
            Column(
                'sticky',
                css_class='small-12 medium-4'
            ),
            Column(
                'announce',
                css_class='small-12 medium-4'
            ),
            Column(
                'closed',
                css_class='small-12 medium-4'
            ),
        ),
    )
    
    # First message is not in edit form
    if not edit_mode:
        fieldsets.append(
            Row(
                Column(
                    'text',
                    css_class='small-12'
                ),
            ),
        )
    
    fieldsets.append(
        Row(
            Column(
                'visible',
                css_class='small-12'
            ),
        ),
    )
    
    # Threadwatch option is not in edit form
    if not edit_mode:
        fieldsets.append(
            Row(
                Column(
                    'threadwatch',
                    css_class='small-12'
                ),
            ),
        )
    
    fieldsets = fieldsets+[
        ButtonHolderPanel(
            Submit('submit', _('Submit')),
            css_class='text-right',
        ),
    ]
    
    helper.layout = Layout(*fieldsets)
    
    return helper

def thread_edit_helper(form_tag=True):
    return thread_helper(form_tag=form_tag, edit_mode=True)



def post_helper(form_tag=True, edit_mode=False):
    """
    Post's form layout helper
    """
    helper = FormHelper()
    helper.form_action = '.'
    helper.attrs = {'data_abide': ''}
    helper.form_tag = form_tag
    
    fieldsets = [
        Row(
            Column(
                'text',
                css_class='small-12'
            ),
        ),
    ]
    
    # Threadwatch option is not in edit form
    if not edit_mode:
        fieldsets.append(
            Row(
                Column(
                    'threadwatch',
                    css_class='small-12'
                ),
            ),
        )
    
    fieldsets = fieldsets+[
        ButtonHolderPanel(
            Submit('submit', _('Submit')),
            css_class='text-right',
        ),
    ]
    
    helper.layout = Layout(*fieldsets)
    
    return helper

def post_edit_helper(form_tag=True):
    return post_helper(form_tag=form_tag, edit_mode=True)

def post_delete_helper(form_tag=True):
    """
    Message's delete form layout helper
    """
    helper = FormHelper()
    helper.form_action = '.'
    helper.attrs = {'data_abide': ''}
    helper.form_tag = form_tag
    
    helper.layout = Layout(
        ButtonHolderPanel(
            Row(
                Column(
                    'confirm',
                    css_class='small-12 medium-8'
                ),
                Column(
                    Submit('submit', _('Submit')),
                    css_class='small-12 medium-4 text-right'
                ),
            ),
        ),
    )
    
    return helper
