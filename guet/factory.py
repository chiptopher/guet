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

from .commands import *


class CommandFactory:
    def __init__(self):
        pass

    def create(self, args: list, command_classes: list = Command.__subclasses__()):
        for command_class in command_classes:
            command = command_class(args)
            if command.validate(args):
                return command
        return HelpCommand(None)
