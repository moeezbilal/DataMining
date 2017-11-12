# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

setup(

    name='HomeWork_1',
    version='1.0',
    description='',
    author='Moeez Jiho',
    license='KTH',
    install_requires=['mmh3'],
    packages=['src'],
)