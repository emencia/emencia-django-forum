
=========
Changelog
=========

Version 0.8.1 - 2015/02/01
**************************

* Fix bad name with moderation permissions for Category and Thread models;

Version 0.8.0 - 2015/01/25
**************************

* Totally removing ``django-guardian`` usage and dependancy. Reasons are:

  * Add a new layer for managing permissions that is difficult to maintain;
  * guardian does not play nice with global permissions and groups, we have to add more code to manage it well;
  * Per-object permissions was a little bit out of the scope of this forum app because it's not a community oriented forum;

* Cleaning documentation from ``django-guardian`` occurences;

Version 0.7.5.2 - 2015/01/12
****************************

* Last try for fixing django-guardian before removing it;
* Fix base template title;

Version 0.7.5.1 - 2015/01/11
****************************

* Fix forgotten typo in parser config name;

Version 0.7.5 - 2015/01/31
**************************

* Fix typo on rst parser config name in default settings;

Version 0.7.4 - 2015/01/06
**************************

* Fix bad template names in threadwatch sending;

Version 0.7.3 - 2014/12/21
**************************

* Fix MANIFEST file for statics;

Version 0.7.2 - 2014/12/21
**************************

* Refactoring templates organization;
* Embed default SCSS sources files and its *compiled* CSS;
* Embed used webfont;

Version 0.7.1 - 2014/11/23
**************************

* Add an optional setting and template to display author's Gravatar in thread's post list using ``django-gravatar2>=1.1.4``;
* Refactoring how we use the crispies within forms;
* Hide some fields for non moderator in thread forms;

Version 0.7 - 2014/11/23
************************

* Remove **rstview** from required dependancy;
* Changing dependancy ``django-crispy-forms >= 1.4.0`` to ``crispy-forms-foundation>=0.3.6`` because we directly this one;
* Changing forms, views and templates to use optional :ref:`text-markup-section`;
* Add shipped stuff (not enabled by default) to use **Django-CodeMirror editor** and **RestructuredText** with the :ref:`text-markup-section` system;
* Moving documentation from README to the ``docs/`` directory, improve it and publish it on `Read the docs <https://readthedocs.org/>`_;
* Update French translation catalog for minor fix;

Version 0.6.8 - 2014/11/11
**************************

* Removes South dependancy;
* Minor improvements on ``forum.utils.ListAppendView`` class view;

Version 0.6.7 - 2014/08/30
**************************

* Move form layouts from ``forum.forms.layouts`` to ``forum.forms.crispies``;
* Fix some bad choices with Permission mixins views;
* Add django-guardian dependancy;

Version 0.6.6 - 2014/08/20
**************************

Add catalog translation for French, this close issue #7.

Version 0.6.5 - 2014/08/20
**************************

Add a view to find and redirect to the exact page where is a Post to have an absolute url working with paginated list, this close issue #5.

Version 0.6.1 - 2014/08/19
**************************

Validate RST syntax on Post message and Category description, this close issue #8.

Version 0.6 - 2014/08/19
************************

* Add 'Django signals' usage when new message is posted so we can use a signal receiver to send email notification;
* Finalize threadwatch with a working email sending and update README for full explanation on threadwatch this close issue #2;

Version 0.5 - 2014/08/17
************************

* Use rstview template filter to render message text into RST, this close issue #3;
* Return 403 response with a rendered template, this close issue #1;
* Update README;

Version 0.4 - 2014/08/16
************************

* Improve README;
* Add the right permission usage with django-guardian;
* Add category and thread moderators;
* Add form confirm into message delete form view;

Version 0.3.1 - 2014/08/12
**************************

* Update package dependancies for missing South entry;
* Update README;

Version 0.3 - 2014/08/12
************************

Update to autobreadcrumbs 1.0 to have the full url's namespace support, use namespaces everywhere

Version 0.2 - 2014/08/11
************************

* Use translation strings for everything;
* Finish templates with Foundation;
* Redo some models to have better modified dates;
* Add initial South migrations;
* Add default settings with pagination;
* Add crispy layouts for all forms;
* Some other minor changes;

Version 0.1 - 2014/08/04
************************

First commit with a working version but not fully integrated.
