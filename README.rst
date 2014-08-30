.. _Django: https://www.djangoproject.com/
.. _South: http://south.readthedocs.org/en/latest/
.. _rstview: https://github.com/sveetch/rstview
.. _autobreadcrumbs: https://github.com/sveetch/autobreadcrumbs
.. _django-braces: https://github.com/brack3t/django-braces/
.. _django-guardian: https://github.com/lukaszb/django-guardian
.. _django-crispy-forms: https://github.com/maraujop/django-crispy-forms

Introduction
============

Yet another Django forum app.

It is simple and more suited for an internal team use (like a company's extranet) than for big public communities. By the way all the view are restricted at less to authenticated users, there is no access for anonymous.

Message content is actually raw text with break line split into paragraph with no escaping, it is planned to use a markup like RST.

Features
--------

* Have categories that contains threads that contains messages;
* Have thread watches: users can subscribe to receive email notification for each new message in a thread;
* Have thread sticky mode and announce mode;
* i18n usage for the interface;
* Use RestructuredText from docutils as markup syntax for messages;
* Global or 'per object' moderation on categories, threads and messages;

Links
-----

* Download his `PyPi package <http://pypi.python.org/pypi/emencia-django-forum>`_;
* Clone it on his `Github repository <https://github.com/emencia/emencia-django-forum>`_;

Requires
--------

* `Django`_ >= 1.5;
* `rstview`_ >= 0.2;
* `autobreadcrumbs`_ >= 1.0;
* `django-braces`_ >= 1.2.0,<1.4;
* `django-crispy-forms`_ >= 1.4.0;
* `django-guardian`_ >= 1.2.0;

Optionnally :

* `South`_ to perform database migrations for next releases;

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

Permission error response
.........................

Permission error is rendered though a ``403.html`` template that is allready embedded within this app, you can override it in your project with adding your custom ``403.html`` template in your project templates directory.

Also you can use another template name, you will have to define its name in ``settings.GUARDIAN_TEMPLATE_403`` (yes, this is a setting from `django-guardian`_, see its doc for more details).

Thread watch
------------

Users can subscribe to watch for new messages on a thread and so they can receive notifications about them.

When a new message is posted on a thread, all users that have subscribed to the thread watch will receive a email except for the message author. ``settings.FORUM_EMAIL_SENDER`` will be used to send emails if defined, else ``settings.DEFAULT_FROM_EMAIL`` will be used instead.

You can change the email subject and content templates used to build the emails :

* ``forum/threadwatch_email_subject.txt`` for the subject;
* ``forum/threadwatch_email_content.txt`` for the content;

These templates receive a context with some variables :

* ``SITE`` : the current Site (from the Django "sites" framework);
* ``thread_instance`` : the thread instance where the message has been posted;
* ``post_instance`` : the message instance that have been posted;


Create your own email sender for notifications
..............................................

This is working with `Django`_ signals, when a new thread message is created, a signal is sended and a receiver is listen to them. The receiver will receive a signal containing some arguments about the message and the thread watchs so it can be used to send email notifications.

The signals usage in this process enables you to make your own receiver to send notifications with your specific email provider/sender or even on another message system (irc, jabber, whatever..).

Default behavior is to use ``forum.signals.new_message_posted_receiver`` that use simple Django email sending and generally it should fit to your needs.

However if you need to have your own receiver, just define the Python path to it, remember that it should be a callable respecting the defined ``kwargs`` and avoid to import Forum models in your code as it will make a circular import error.

An example in your settings to use your own receiver : ::

    FORUM_NEW_POST_SIGNAL = 'myproject.signals.mycallback'

And a receiver example : ::

    def new_message_posted_receiver(sender, **kwargs):
        message = kwargs['post_instance']
        threadwatchs = kwargs['threadwatchs']
        
        print "New message #{0} has been posted on thread:".format(message.id), message.thread
        
        for item in threadwatchs:
            print "*", item, "for", item.owner

See ``forum.signals.new_message_posted_receiver`` to have a real example and don't forget to read about signals in the Django documentation.