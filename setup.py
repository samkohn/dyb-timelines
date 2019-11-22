'''
The setup.py file for dyb-timelines.

'''

from setuptools import setup, find_packages
from codecs import open
import os

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(os.path.join(here, 'VERSION')) as f:
    version = f.read()

setup(
        name='dyb-timelines',
        version=version,
        description='Draw timelines of Daya Bay events',
        long_description=long_description,
        long_description_content_type="text/markdown",
        url='https://github.com/samkohn/dyb-timelines',
        author='Sam Kohn',
        author_email='skohn@lbl.gov',
        keywords='daya bay dyb physics',
        packages=[],
        py_modules=['draw_timeline'],
        install_requires=[
            'reportlab',
            ],
)
