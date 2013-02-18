from setuptools import setup, find_packages
import os

version = '1.0b1'

setup(name='genweb.upc',
      version=version,
      description="Genweb UPC features package",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.rst")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='genweb upc',
      author='UPCnet Plone Team',
      author_email='plone.team@upcnet.es',
      url='https://github.com/upcnet/genweb.upc',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['genweb', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
      ],
      extras_require={'test': ['plone.app.testing']},
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
