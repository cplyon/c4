from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
   name='c4',
   version='1.0',
   description='A simple, text-based Connect-4 game',
   license="MIT",
   long_description=long_description,
   author='Chris Lyon',
   author_email='chris@cplyon.ca',
   packages=['c4'],
   install_requires=[''],
)
