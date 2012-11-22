from setuptools import setup, find_packages
import os

version = '2.4.2.dev0'
maintainer = 'Mathias Leimgruber'

tests_require = [
    'unittest2',
    'mocker',
    'ftw.testing',
    'plone.testing',
    'plone.app.testing',

    'transaction',
    'zope.configuration',
    'zope.traversing',
    'Products.CMFPlone',
    'Products.Five',
    'Products.GenericSetup',

    'ftw.workspace',
    'ftw.pdfgenerator',
    ]

extras_require = {
    'tests': tests_require,

    'pdf': [
        'ftw.pdfgenerator',
        ],

    'workspace': [
        'ftw.workspace',
        ]}

setup(name='ftw.task',
      version=version,
      description='A simple task content type for Plone.',
      long_description=open('README.rst').read() + '\n' + \
          open(os.path.join('docs', 'HISTORY.txt')).read(),

      # Get more strings from
      # http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Plone',
        'Framework :: Plone :: 4.1',
        'Framework :: Plone :: 4.2',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],

      keywords='ftw task plone',
      author='4teamwork GmbH',
      author_email='mailto:info@4teamwork.ch',
      maintainer=maintainer,
      url='https://github.com/4teamwork/ftw.task',
      license='GPL2',

      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw', ],
      include_package_data=True,
      zip_safe=False,

      install_requires=[
        'setuptools',

        # Zope
        'AccessControl',
        'Zope2',
        'zope.app.component',
        'zope.component',
        'zope.i18n',
        'zope.i18nmessageid',
        'zope.interface',
        'zope.schema',

        # Plone
        'Products.ATContentTypes',
        'Products.Archetypes',
        'Products.CMFCore',
        'Products.ATReferenceBrowserWidget',
        'plone.principalsource',
        'plone.app.contentmenu',
        'plone.app.portlets',
        'plone.portlets',

        # Addons
        'ftw.calendarwidget',
        'ftw.upgrade',
        ],

      tests_require=tests_require,
      extras_require=extras_require,

      test_suite = 'ftw.task.tests.test_docs.test_suite',
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
