.. _autobreadcrumbs: http://pypi.python.org/pypi/autobreadcrumbs
.. _Django: https://www.djangoproject.com/
.. _django-braces: https://github.com/sveetch/django-braces
.. _django-guardian: https://github.com/lukaszb/django-guardian
.. _django-crispy-forms: https://github.com/maraujop/django-crispy-forms

Introduction
============

Yet another Django forum app.

It is simple and more suited for an internal team use (like a company's extranet) than for big public communities. By the way all the view are restricted at less to authenticated users, there is no access for anonymous.

Message content is actually raw text with break line split into paragraph with no escaping, it is planned to use a markup like RST.

Features
........

* Have categories that contains threads that contains messages;
* Have thread watches: users can subscribe to receive email notification for each new message in a thread;
* Have thread sticky mode and announce mode;
* i18n usage for the interface;
* Global or 'per object' moderation on categories, threads and messages;

TODO
----

* Return 403 response with rendered template, not an empty 403 response;
* Redo mail sending for thread watchs;
* Use a lightweight RST as markup syntax in object descriptions and messages;
* Sticky mode, announce mode, closed and visible options must be available only for moderators;
* Split some template parts to overrides them without to overrides the whole templates (like for autobreadcrumb usage and to not make it a package dependancy);
* Resolve bug with "Messages pagination in 'Thread detail' view" and 'Post.get_absolute_url()';
* When big features are implemented and app stabilized, optimize SQL requests usage and use spaceless tag in templates;
* Queue email notification for Cron usage ?

Links
-----

* Download his `PyPi package <http://pypi.python.org/pypi/emencia-django-forum>`_;
* Clone it on his `Github repository <https://github.com/emencia/emencia-django-forum>`_;

Requires
--------

* `Django`_ >= 1.5;
* `autobreadcrumbs`_ >= 1.0;
* `django-braces`_ >= 1.2.0,<1.4;
* `django-crispy-forms`_ >= 1.4.0;
* `django-guardian`_ >=1.2.0;

Install
=======

Add it to your installed apps in settings : ::

    INSTALLED_APPS = (
        ...
        'autobreadcrumbs',
        'guardian',
        'forum',
        ...
    )

Add its settings (in your project settings) :

::

    from forum.settings import *

(Also you can override some of its settings, see ``forum.settings``).

Add `django-guardian`_ settings (see its doc for more details) :

::

    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend', # this is default
        'guardian.backends.ObjectPermissionBackend',
    )

    ANONYMOUS_USER_ID = None

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

If you don't want to use it you have two choices :

* Simply ignore it, it will be used for automatic page titles but just override forum's base template to remove it;
* If you don't install it, you will have to remove it from your settings and urls, then overrides all forum's template that use its tags;

Usage
=====

Permissions
-----------

The forum make usage of `django-guardian`_ to manage 'per object permissions' or 'global permissions'.

Actually you need to use the Django admin and be a staff user with the right permissions for managing forum objects to add these permissions for your users.

And so, you can add the needed permissions globally to the whole forum within each user accounts. Or you can add a permission for a specific object its edit page using the link named *Object permissions*.

* Users with ``forum.add_category`` permissions can create categories;
* All users can create a new thread;
* All users can add a new message to a thread that is visible and not closed;
* Users with ``forum.moderate_category`` can edit them and can manage (edit, delete) their threads parameters and messages. They are called *Category moderators*;
* Users with ``forum.moderate_thread`` can edit thread parameters, edit thread messages and delete thread messages. They are called *Thread moderators*;
* Users have permission to edit their own message if ``settings.FORUM_OWNER_MESSAGE_CAN_EDIT`` is True;


Others Category's and Thread's model permissions have no roles on frontend.
