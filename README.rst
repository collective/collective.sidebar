.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.


==================
collective.sidebar
==================

A sidebar for Plone to consolidate toolbar and navigation.

.. image:: https://raw.githubusercontent.com/collective/collective.sidebar/master/docs/screenshot.png
    :target: https://raw.githubusercontent.com/collective/collective.sidebar/master/docs/screenshot.png


Mostly Harmless
---------------

.. build status

.. image:: https://img.shields.io/github/workflow/status/collective/collective.sidebar/Build/master?label=Build
   :target: https://github.com/collective/collective.sidebar/actions/workflows/build.yml
   :alt: Build Status

.. coverage

.. image:: https://coveralls.io/repos/github/collective/collective.sidebar/badge.svg?branch=master
    :target: https://coveralls.io/github/collective/collective.sidebar?branch=master
    :alt: Code Coverage

.. pypi version

.. image:: https://img.shields.io/pypi/v/collective.sidebar.svg?label=PyPI
    :target: https://pypi.python.org/pypi/collective.sidebar/
    :alt: Latest Version

.. supported python versions

.. image:: https://img.shields.io/pypi/pyversions/collective.sidebar.svg?label=Python
    :target: https://pypi.python.org/pypi/collective.sidebar/
    :alt: Supported Python Versions

.. licence

.. image:: https://img.shields.io/pypi/l/collective.sidebar.svg?label=Licence
    :target: https://pypi.python.org/pypi/collective.sidebar/
    :alt: License

Features
--------

- Responsive mobile first Sidebar for Plone
- Toolbar and navigation in one place
- Dynamic navigation without reload
- Drop in replacement for Plone toolbar
- Includes site navigation
- Includes add, edit and display functions
- Includes workflow state management
- Includes quick access to the user profile
- Includes configurable persistent site links via actions


Demo
----

- https://plonetheme.tokyo/
- https://www.operun.de/


Documentation
-------------

Full documentation for end users can be found in the "docs" folder.


Credits
-------

This package is developed and maintained by `operun Digital Solutions <https://www.operun.de>`_. Check out other `projects <https://www.operun.de/projekte>`_ we developed based on the `Enterprise Content Management System <https://www.operun.de/produkte/enterprise-content-management-system>`_ Plone.


Translations
------------

This product has been translated into:

- German (thanks, santonelli)


Installation
------------

Install collective.sidebar by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.sidebar


and then running ``bin/buildout``...


Versions
--------

- Version 1.x works with Plone 5.2
- Version 2.x works with Plone 6


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.sidebar/issues
- Source Code: https://github.com/collective/collective.sidebar


Support
-------

If you are having issues, please let us know. We have a issue tracker located at: https://github.com/collective/collective.sidebar/issues


Change Icon Font
-----------------

When you installed Font Awesome or Fontello, you can change the sidebar to use these icons.
First choose the icon font in the control panel.
Then change the sidebar static links in the ZMI or via actions.xml.


License
-------

The project is licensed under the GPLv2.
