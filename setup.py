# -*- coding: utf-8 -*-
"""
This module contains the tool of ftw.task
"""
from setuptools import setup, find_packages

def read(*rnames):
    return open('/'.join(rnames)).read()

version = open('ftw/task/version.txt').read().strip()
maintainer = 'Victor Baumann'

long_description = (
    read('README.txt')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' +
    read('docs', 'HISTORY.txt')
    + '\n' +
    'Detailed Documentation\n'
    '**********************\n'
    + '\n' +
    read('ftw', 'task', 'README.txt')
    + '\n' +
    'Download\n'
    '********\n'
    )

tests_require = [
    'collective.testcaselayer',
    ]

setup(name='ftw.task',
      version=version,
      description="Task type (Maintainer: %s)" % maintainer,
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Plone',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
      keywords='plone archetype ftw',
      author='%s, 4teamwork GmbH' % maintainer,
      author_email='mailto:info@4teamwork.ch',
      maintainer=maintainer,
      url='http://psc.4teamwork.ch/4teamwork/kunden/ftw/ftw.task/',
      license='GPL2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
        'Products.ATReferenceBrowserWidget',
                        'plone.principalsource',
                        # -*- Extra requirements: -*-
                        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite = 'ftw.task.tests.test_docs.test_suite',
      entry_points="""
      # -*- entry_points -*- 
      """,
      )
