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
          'guet.commands.decorators',
          'guet.commands.scriptcommands',
          'guet.commands.scriptcommands.commitmsg',
          'guet.commands.scriptcommands.postcommit',
          'guet.commands.scriptcommands.precommit',
          'guet.commands.strategies',
          'guet.commands.usercommands',
          'guet.commands.usercommands.get',
          'guet.commands.usercommands.addcommitter',
          'guet.commands.usercommands.init',
          'guet.commands.usercommands.start',
          'guet.commands.usercommands.remove',
          'guet.commands.usercommands.config',
          'guet.commands.usercommands.config',
          'guet.commands.usercommands.config',
          'guet.commands.usercommands.help',
          'guet.commands.usercommands.setcommitters',
          'guet.committers',
          'guet.hooks',
          'guet.files',
          'guet.settings',
          'guet.git',
          'guet.config',
          'guet.context',
          'guet.util'
      ])
