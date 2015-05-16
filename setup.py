from setuptools import setup


setup(
    name='knights-templater',
    version='1.2',
    packages=[
        'knights',
        'knights.compat',
    ],
    author='Curtis Maloney',
    author_email='curtis@tinbrain.net',
    description='A simple AST-based Python Template engine.',
    keywords='template',
    url='http://github.com/funkybob/knights-templater/',
)
