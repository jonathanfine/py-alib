# Based upon https://github.com/pypa/sampleproject/blob/master/setup.py

# Copied from pypa/sampleproject
from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()
# End of copied from pypa/sampleproject

setup(
    name = 'alib',
    packages = ['alib'],
    version = '0.0.1a1',        # First alpha release - see PEP440.
    description = 'A LIB-rary of useful Python code',
    long_description = long_description,
    author = 'Jonathan Fine',
    author_email = 'jfine@pytex.org',
    url = 'https://github.com/jonathanfine/py-alib',
    keywords = ['testing'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ],
)
