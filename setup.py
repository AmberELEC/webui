#!/usr/bin/env python3

from setuptools import setup
setup(name='amberelec-webui',
      version='1.0',
      description='Web Interface for AmberElLEC',
      author='benphelps',
      author_email='bphelpsen@gmail.com',
      url='https://github.com/AmberELEC/webui',
      license='GPLv2+',
      platforms=['Linux'],
      install_requires=['ftfy', 'bottle', 'python_pam', 'beaker']
      )
