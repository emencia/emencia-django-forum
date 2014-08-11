"""
Here we try to safely use crispy_form if installed
"""
import warnings

from django.utils.importlib import import_module
from django.utils.translation import ugettext as _

# Try to import crispy_form base stuff to use for the default helper
try:
    from crispy_forms.helper import FormHelper
    from crispy_forms.layout import Submit
except ImportError:
    def default_helper():
        return None
else:
    def default_helper(form_tag=True):
        helper = FormHelper()
        helper.form_action = '.'
        helper.form_tag = form_tag
        helper.add_input(Submit('submit', _('Submit')))
        return helper


def get_form_helper(helper_path, default=None):
    """
    Try to import the specified helper from the given Python path
    
    @helper_path is a string containing a Python path to the wanted helper, @default is 
    a callable used as the default layout if the @helper_path import fails. @default 
    could be None if you don't want a default layout (and use the automated one 
    from crispy_forms).
    
    You should only use the None value for @default if you don't plan to use crispy_forms.
    
    Return a callable or None
    """
    if helper_path is None:
        return default
    
    dot = helper_path.rindex('.')
    module_name = helper_path[:dot]
    class_name = helper_path[dot + 1:]
    try:
        _class = getattr(import_module(module_name), class_name)
        return _class
    except (ImportError, AttributeError):
        warnings.warn('%s cannot be imported' % helper_path,
                      RuntimeWarning)
    return default


class CrispyFormMixin(object):
    """
    Embed the technic in a form mixin to use crispy-form and safely fallback if not installed
    """
    crispy_form_helper_path = None # Custom layout method path
    crispy_form_tag = True
    
    def __init__(self, *args, **kwargs):
        # Specified helper if any (and import succeed)
        helper = get_form_helper(self.crispy_form_helper_path, default=default_helper)
        if helper is not None:
            self.helper = helper(form_tag=self.crispy_form_tag)
        else:
            # Default helper
            self.helper = default_helper(form_tag=self.crispy_form_tag)
