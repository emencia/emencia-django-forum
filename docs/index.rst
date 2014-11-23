.. _Django: https://www.djangoproject.com/
.. _South: http://south.readthedocs.org/en/latest/
.. _rstview: https://github.com/sveetch/rstview
.. _autobreadcrumbs: https://github.com/sveetch/autobreadcrumbs
.. _django-braces: https://github.com/brack3t/django-braces/
.. _django-guardian: https://github.com/lukaszb/django-guardian
.. _django-crispy-forms: https://github.com/maraujop/django-crispy-forms
.. _Django-CodeMirror: https://github.com/sveetch/djangocodemirror
.. _RestructuredText: http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html

Welcome to Emencia Django Forum's documentation!
================================================

Yet another Django forum app.

It is simple and more suited for an internal team use (like a company's extranet) than for big public communities. By the way all the view are restricted at less to authenticated users, there is no access for anonymous.

Features
********

* Have **categories** that contains **threads** that contains **messages**;
* Have **thread watches**: users can subscribe to receive email notification for each new message in a thread, see :ref:`threadwatch-section`;
* Have thread **sticky mode** and **announce mode**;
* **i18n** usage for the interface;
* Global or **'per object' moderation** on categories, threads and messages, see :ref:`permissions-section`;
* Optional **markup syntax** for messages, default is `RestructuredText`_ from docutils but you can use your own, see :ref:`text-markup-section`;
* Optional **DjangoCodeMirror editor** or your own editor if you want, see :ref:`text-markup-section`;

Links
*****

* Read the documentation on `Read the docs <https://emencia-django-forum.readthedocs.org/>`_;
* Download his `PyPi package <http://pypi.python.org/pypi/emencia-django-forum>`_;
* Clone it on his `Github repository <https://github.com/emencia/emencia-django-forum>`_;

Requires
********

* `Django`_ >= 1.5;
* `autobreadcrumbs`_ >= 1.0;
* `django-braces`_ >= 1.2.0,<1.4;
* `django-crispy-forms`_ >= 1.4.0;
* `django-guardian`_ >= 1.2.0;

Optionnally
-----------

* `South`_ to perform database migrations for next releases;
* If you want to use the shipped :ref:`text-markup-section` integration :

    * `rstview`_ >= 0.2;
    * `Django-CodeMirror`_ >= 0.9.7;


Table of contents
*****************

.. toctree::
   :maxdepth: 2
   
   install.rst
   usage.rst
   changelog.rst
