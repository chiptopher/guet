import guet
from setuptools import setup

setup(
    name='guet',
    version=guet.__version__,
    description='Enable contribution tracking when pair programming',
    url='https://github.com/chiptopher/guet',
    keywords='pair programming',
    entry_points={
        'console_scripts': [
            'guet=guet.main:main'
        ]
    },
    packages=[
      'guet',
      'guet.commands'
    ]
)
