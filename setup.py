from setuptools import setup

import guet

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='guet',
      version=guet.__version__,
      description='Enable contribution tracking when pair programming',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/chiptopher/guet',
      keywords='pair programming',
      entry_points={'console_scripts': ['guet=guet.main:main']},
      packages=[
          'guet',
          'guet.commands',
          'guet.commands.add',
          'guet.commands.get',
          'guet.commands.help',
          'guet.commands.init',
          'guet.commands.remove',
          'guet.commands.set',
          'guet.committers',
          'guet.config',
          'guet.files',
          'guet.git',
          'guet.hooks',
          'guet.settings',
          'guet.steps',
          'guet.steps.action',
          'guet.steps.check',
          'guet.steps.preparation',
          'guet.util'
      ])
