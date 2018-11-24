"""
Copyright 2018 Christopher M. Boyer

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import importlib
import inspect

from .commands.command import Command


def get_command_subclasses(ignored_command_classes: list = []):
    classmap = dict()
    base_module = 'guet.commands'
    module = importlib.import_module(base_module)
    for attr in dir(module):
        classmodulename = '{}.{}'.format(base_module, attr)
        try:
            classmodule = importlib.import_module(classmodulename)
            clsmembers = inspect.getmembers(classmodule, inspect.isclass)
            for clsmember in clsmembers:
                if issubclass(clsmember[1], Command):
                    classmap[clsmember[0]] = clsmember[1]
        except ModuleNotFoundError:
            pass
    classlist = []
    for cls in classmap.values():
        if cls is Command or cls in ignored_command_classes:
            pass
        else:
            classlist.append(cls)
    return classlist
