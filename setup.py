#coding: utf-8

import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-odesk-auth',
    version='0.2-pre2',
    packages=['django_odesk_auth'],
    include_package_data=True,
    license='BSD License',
    description='A simple Django app for basic “Log in via Upwork” functionality.',
    long_description=README,
    author='Upwork',
    author_email='python@upwork.com',
    maintainer='Anton Strogonoff',
    maintainer_email='anton@strogonoff.name',
    download_url='http://github.com/strogonoff/django-odesk-auth',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
