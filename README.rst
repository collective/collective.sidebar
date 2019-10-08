.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

.. image:: https://travis-ci.org/collective/collective.sidebar.svg?branch=master
    :target: https://travis-ci.org/collective/collective.sidebar

.. image:: https://coveralls.io/repos/github/collective/collective.sidebar/badge.svg?branch=master
    :target: https://coveralls.io/github/collective/collective.sidebar?branch=master

.. image:: https://badge.fury.io/py/collective.sidebar.svg
    :target: https://badge.fury.io/py/collective.sidebar


==================
collective.sidebar
==================

A sidebar for Plone to consolidate toolbar and navigation.

.. image:: https://raw.githubusercontent.com/collective/collective.sidebar/master/docs/screenshot.png
    :target: https://raw.githubusercontent.com/collective/collective.sidebar/master/docs/screenshot.png


Features
--------

- Replaces the default Plone toolbar
- Inherits structureupdater pattern
- Includes workflow state management
- Includes site navigation
- Includes quick access to the user profile
- Includes configurable persistent site links through the ZMI


Examples
--------

- TBD


Documentation
-------------

Full documentation for end users can be found in the "docs" folder.


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
