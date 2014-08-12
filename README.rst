.. _autobreadcrumbs: http://pypi.python.org/pypi/autobreadcrumbs
.. _Django: https://www.djangoproject.com/
.. _django-braces: https://github.com/sveetch/django-braces
.. _django-crispy-forms: https://github.com/maraujop/django-crispy-forms

Introduction
============

Yet another Django forum app.

* Simple;
* More suited for an internal team use (like a company's extranet) than for big public communities;
* Have categories that contains threads that contains messages;
* Have thread watches;
* Have thread sticky mode and announce mode;
* i18n usage for the interface;

TODO
----

* Apply rights permissions (like for admin views only);
* Redo mail sending for thread watchs;
* Use a lightweight RST as markup syntax in object descriptions and messages;
* Split some template parts to overrides them without to overrides the whole templates (like for autobreadcrumb usage and to not make it a package dependancy);

Links
-----

* Download his `PyPi package <http://pypi.python.org/pypi/emencia-django-forum>`_;
* Clone it on his `Github repository <https://github.com/emencia/emencia-django-forum>`_;

Requires
--------

* `Django`_ >= 1.5;
* `autobreadcrumbs`_ >= 1.0;
* `django-braces`_ >=1.2.0,<1.4;
* `django-crispy-forms`_ >= 1.4.0;

Install
=======

Add it to your installed apps in settings : ::

    INSTALLED_APPS = (
        ...
        'autobreadcrumbs'
        'forum'
        ...
    )

Add its settings (in your project settings) :

::

    from forum.settings import *

(Also you can override some of its settings, see ``forum.settings``).

Then register `autobreadcrumbs`_ *context processor* in settings :

::

    TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        'autobreadcrumbs.context_processors.AutoBreadcrumbsContext',
        ...
    )


Finally mount its urls and add the `autobreadcrumbs`_ *autodiscover* in your main ``urls.py`` : ::

    import autobreadcrumbs
    autobreadcrumbs.autodiscover()

    urlpatterns = patterns('',
        ...
        (r'^forum/', include('forum.urls', namespace='forum')),
        ...
    )

About autobreadcrumbs
---------------------

If you don't want to use it you have to choices :

* Simply ignore it;
* If you don't install it, you will have to remove it from your settings and urls, then overrides all forum's template that use its tags;
