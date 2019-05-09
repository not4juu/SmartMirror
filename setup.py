from setuptools import setup
from sys import version, exit


if version < '3.5.0':
    print("THIS MODULE REQUIRES PYTHON 3.5.0 > YOU ARE CURRENTLY USING PYTHON {0}".format(version))
    exit(1)

with open('requirements.txt') as f:
    install_requires = f.read().strip().split('\n')

setup(
    name='SmartMirror',
    version='1.0.0',
    packages=['tests', 'smartmirror'],
    url='https://github.com/not4juu/SmartMirror',
    license=open('LICENSE').read(),
    author='not4juu',
    author_email='Sebastian.Kaluzny@fis.agh.edu.pl',
    description='Smart Mirror for Raspberry pi 3',
    long_description=open('README.md').read(),
    install_requires=install_requires,
)
