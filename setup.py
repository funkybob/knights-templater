from setuptools import setup, find_packages


setup(
    name='knights-templater',
    version='1.0',
    packages=find_packages(exclude=('tests.*',)),
    author='Curtis Maloney',
    author_email='curtis@tinbrain.net',
    description='A simple AST-based Python Template engine.',
    keywords='template',
    url='http://github.com/funkybob/knights-templater/',
)
