.. _Django: https://www.djangoproject.com/
.. _South: http://south.readthedocs.org/en/latest/
.. _rstview: https://github.com/sveetch/rstview
.. _autobreadcrumbs: https://github.com/sveetch/autobreadcrumbs
.. _django-braces: https://github.com/brack3t/django-braces/
.. _django-crispy-forms: https://github.com/maraujop/django-crispy-forms
.. _Django-CodeMirror: https://github.com/sveetch/djangocodemirror
.. _RestructuredText: http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html

Emencia Django Forum
====================

It is simple and more suited for an internal team use (like a company's extranet) than for big public communities. By the way all the view are restricted at less to authenticated users, there is no access for anonymous.

Features
********

* Have **categories** that contains **threads** that contains **messages**;
* Have **thread watches**: users can subscribe to receive email notification for each new message in a thread;
* Have thread **sticky mode** and **announce mode**;
* **i18n** usage for the interface;
* Permissions usage for moderation on categories, threads and messages;
* Optional **markup syntax** for messages, default is `RestructuredText`_ from docutils but you can use your own;
* Optional **DjangoCodeMirror editor** or your own editor if you want;

Links
*****

* Read the documentation on `Read the docs <https://emencia-django-forum.readthedocs.org/>`_;
* Download his `PyPi package <http://pypi.python.org/pypi/emencia-django-forum>`_;
* Clone it on his `Github repository <https://github.com/emencia/emencia-django-forum>`_;
