import os

from setuptools import setup

# Utility function to read files. Used for the long_description.
def read(fname):
      return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='osdf-python',
      description='Python client to Open Science Data Framework (OSDF) REST servers.',
      long_description='The Open Science Data Framework (OSDF) is a specialized ' + \
                       'document database that allows users to store, retrieve, ' + \
                       'query and track changes to data over time easily. ' + \
                       'Because the API uses JSON and REST, developers are ' + \
                       'able to use OSDF in the language of their choice ' + \
                       'because almost every language has support for ' + \
                       'communications via HTTP and working with JSON.',
      version='0.8',
      py_modules=['osdf', 'request'],
      author='Victor Felix',
      author_email='victor73@github.com',
      url='http://osdf.igs.umaryland.edu',
      license='MIT',
      install_requires=['jsondiff'],
      scripts = [
          'bin/osdf'
      ],
      classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 2.7",
        "Topic :: Utilities",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Bio-Informatics"
      ]
     )
