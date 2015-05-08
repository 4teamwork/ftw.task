Introduction
------------

``ftw.task`` provides a simple task content type for Plone.

.. figure:: http://onegov.ch/approved.png/image
   :align: right
   :target: http://onegov.ch/community/zertifizierte-module/ftw.task

   Certified: 01/2013

Compatiblity
------------

**Workspace / PDF**: When installed with with `ftw.workspace`_ and `ftw.pdfgenerator`_
it provides a listing in the workspace details PDF.


Usage
-----

- Add the package to your buildout configuration:

::

    [instance]
    eggs +=
        ...
        ftw.task

- Install the generic setup profile.


Links
-----

- Github: https://github.com/4teamwork/ftw.task
- Issues: https://github.com/4teamwork/ftw.task/issues
- Pypi: http://pypi.python.org/pypi/ftw.task
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.task


Copyright
---------

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.task`` is licensed under GNU General Public License, version 2.

.. _ftw.workspace: http://github.com/4teamwork/ftw.workspace
.. _ftw.pdfgenerator: http://github.com/4teamwork/ftw.pdfgenerator
