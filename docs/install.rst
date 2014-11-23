.. _Django: https://www.djangoproject.com/
.. _South: http://south.readthedocs.org/en/latest/
.. _rstview: https://github.com/sveetch/rstview
.. _autobreadcrumbs: https://github.com/sveetch/autobreadcrumbs
.. _django-braces: https://github.com/brack3t/django-braces/
.. _django-guardian: https://github.com/lukaszb/django-guardian
.. _django-crispy-forms: https://github.com/maraujop/django-crispy-forms
.. _Django-CodeMirror: https://github.com/sveetch/djangocodemirror

=======
Install
=======

Add it to your installed apps in settings :

.. sourcecode:: python

    INSTALLED_APPS = (
        ...
        'autobreadcrumbs',
        'guardian',
        'forum',
        ...
    )

Add its settings (in your project settings) :

.. sourcecode:: python

    from forum.settings import *

(Also you can override some of its settings, see ``forum.settings`` for more details).

Add `django-guardian`_ settings (see its doc for more details) :

.. sourcecode:: python

    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend', # this is default
        'guardian.backends.ObjectPermissionBackend',
    )

    ANONYMOUS_USER_ID = None

Then register `autobreadcrumbs`_ *context processor* in settings :

.. sourcecode:: python

    TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        'autobreadcrumbs.context_processors.AutoBreadcrumbsContext',
        ...
    )


Finally mount its urls and add the `autobreadcrumbs`_ *autodiscover* in your main ``urls.py`` :

.. sourcecode:: python

    import autobreadcrumbs
    autobreadcrumbs.autodiscover()

    urlpatterns = patterns('',
        ...
        (r'^forum/', include('forum.urls', namespace='forum')),
        ...
    )

About autobreadcrumbs
*********************

`autobreadcrumbs`_ automatically build the bread crumbs from the current page path.

If you don't want to use it, you have two choices :

* Simply ignore it, it will be used for automatic page titles but just override forum's base template to remove it;
* If you don't install it, you will have to remove it from your settings and urls, then overrides all forum's template that use its tags;

.. _text-markup-section:

Text markup
***********

Default behavior configured in settings is to not use any Markup syntax usage.

But if you want you can configure some settings to use a Markup syntax renderer and a form field to use a specific editor.

This can be done with the following settings :

.. sourcecode:: python

    # Text markup renderer
    FORUM_TEXT_MARKUP_RENDER = None # Default, just a CharField

    # Field helper for text in forms
    FORUM_TEXT_FIELD_HELPER_PATH = None # Default, just a CharField

    # Template to init some Javascript for text in forms
    FORUM_TEXT_FIELD_JS_TEMPLATE = None # Default, no JS template

    # Validator helper for Post.text in forms
    FORUM_TEXT_VALIDATOR_HELPER_PATH = None # Default, no markup validation

They are the default values in the forum settings.
    
Explanations
------------

**FORUM_TEXT_FIELD_HELPER_PATH**
    a function that will be used to define a form field to use for text. 
    
    Signature is ``get_text_field(form_instance, **kwargs)`` where :
    
    * ``form_instance`` is the Form instance where it will be used from;
    * ``kwargs`` is a dict containing all default named arguments to give to the field. These default arguments are ``label`` for the field label name and ``required``  that is ``True`` (you should never change this);
    
    This should return an instanciated form field that must act as a ``CharField``.

**FORUM_TEXT_VALIDATOR_HELPER_PATH**

    A function that will be used to clean value on the form field text;
    
    Signature is ``clean_restructuredtext(form_instance, content)`` where :
    
    * ``form_instance`` is the Form instance where it will be used from;
    * ``content`` is the value to validate;
    
    This should return a string value.
    
**FORUM_TEXT_MARKUP_RENDER_TEMPLATE**

    A template to include to render text value with some markup syntax. It will have access to the page context with an additional value named ``content`` that will be the text to render;

**FORUM_TEXT_FIELD_JS_TEMPLATE**

    A template to include with forms when your custom form field require some Javascript to initialize it. It will have access to page context with an additional value named ``field`` that will be the targeted form field;

All these settings are only used with forms and template managing ``forum.models.Post.text`` and ``forum.models.Category.description`` models attributes.
    
Example
-------

There are the settings to use the shipped Markup syntax renderer and editor, disabled by default but that you can easily enable in your settings :

.. sourcecode:: python

    # Field helper for text in forms
    FORUM_TEXT_FIELD_HELPER_PATH = "forum.markup.get_text_field" # Use DjangoCodeMirror

    # Validator helper for Post.text in forms
    FORUM_TEXT_VALIDATOR_HELPER_PATH = "forum.markup.clean_restructuredtext" # Validation for RST syntax (with Rstview)

    # Template to init some Javascript for text in forms
    FORUM_TEXT_FIELD_JS_TEMPLATE = "forum/_text_field_djangocodemirror_js.html" # Use DjangoCodeMirror

    # Text markup renderer
    FORUM_TEXT_MARKUP_RENDER_TEMPLATE = "forum/_text_markup_render.html" # Use Rstview renderer

Read their source code to see how they work in detail.

.. warning:: Before enabling these settings you must install `rstview`_ and `Django-CodeMirror`_.