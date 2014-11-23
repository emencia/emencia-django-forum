.. _Django: https://www.djangoproject.com/
.. _South: http://south.readthedocs.org/en/latest/
.. _rstview: https://github.com/sveetch/rstview
.. _autobreadcrumbs: https://github.com/sveetch/autobreadcrumbs
.. _django-braces: https://github.com/brack3t/django-braces/
.. _django-guardian: https://github.com/lukaszb/django-guardian
.. _django-crispy-forms: https://github.com/maraujop/django-crispy-forms
.. _Django-CodeMirror: https://github.com/sveetch/djangocodemirror

=====
Usage
=====

.. _permissions-section:

Permissions
***********

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
-------------------------

Permission error is rendered though a ``403.html`` template that is allready embedded within this app, you can override it in your project with adding your custom ``403.html`` template in your project templates directory.

Also you can use another template name, you will have to define its name in ``settings.GUARDIAN_TEMPLATE_403`` (this is a setting from `django-guardian`_, see its documentation for more details).

.. _threadwatch-section:

Thread watch
************

Users can subscribe to watch for new messages on a thread and so they can receive notifications about them.

When a new message is posted on a thread, all users that have subscribed to the thread watch will receive an email, excepting for the message author himself. 

``settings.FORUM_EMAIL_SENDER`` will be used to send emails if defined, else ``settings.DEFAULT_FROM_EMAIL`` will be used instead.

You can change the email subject and content templates used to build the emails :

* ``forum/threadwatch_email_subject.txt`` for the subject;
* ``forum/threadwatch_email_content.txt`` for the content;

These templates receive a context with some variables :

* ``SITE`` : the current Site (from the Django "sites" framework);
* ``thread_instance`` : the thread instance where the message has been posted;
* ``post_instance`` : the message instance that have been posted;


Create your own email sender for notifications
----------------------------------------------

This is working with `Django`_ signals, when a new thread message is created, a signal is sended and a receiver is listen to them. The receiver will receive a signal containing some arguments about the message and the thread watchs so it can be used to send email notifications.

The signals usage in this process enable you to make your own receiver to send notifications with your specific email provider/sender or even on another message system (irc, jabber, whatever..).

Default behavior is to use ``forum.signals.new_message_posted_receiver`` that use simple Django email sending and generally it should fit to your needs.

However if you need to have your own receiver, just define the Python path to it, remember that it should be a callable respecting the defined ``kwargs`` and avoid to import Forum models in your code as it will make a circular import error.

An example in your settings to use your own receiver :

.. sourcecode:: python

    FORUM_NEW_POST_SIGNAL = 'myproject.signals.mycallback'

And a receiver example :

.. sourcecode:: python

    def new_message_posted_receiver(sender, **kwargs):
        message = kwargs['post_instance']
        threadwatchs = kwargs['threadwatchs']
        
        print "New message #{0} has been posted on thread:".format(message.id), message.thread
        
        for item in threadwatchs:
            print "*", item, "for", item.owner

See ``forum.signals.new_message_posted_receiver`` to have a real example and don't forget to read about signals in the Django documentation.