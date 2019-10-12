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
from guet.gateways.io import PrintGateway, InputGateway
from guet.commands.command import Command
from guet.git.any_hooks_present import any_hooks_present
from guet.git.git_path_from_cwd import git_hook_path_from_cwd
from guet.git.create_hook import create_hook, HookMode, Hooks
from guet.git.git_present_in_cwd import git_present_in_cwd


class StartCommand(Command):
    _REQUIRED_ARGS_IN_CORRECT_ORDER = ['start']

    def __init__(self,
                 args,
                 print_gateway: PrintGateway = PrintGateway(),
                 input_gateway: InputGateway = InputGateway()):
        super().__init__(args, print_gateway)
        self._input_gateway = input_gateway

    def execute(self):
        if git_present_in_cwd():
            hook_path = git_hook_path_from_cwd()
            if not any_hooks_present(hook_path):
                self._create_all_hooks(hook_path, HookMode.NEW_OR_OVERWRITE)
            else:
                hook_mode = None
                self._print_gateway.print('There is already commit hooks in this project. Would you like to overwrite (o), create (c) the file and put it in the hooks folder, or cancel (x)?')
                val = self._input_gateway.input()
                if val == 'o':
                    hook_mode = HookMode.NEW_OR_OVERWRITE
                elif val == 'c':
                    hook_mode = HookMode.CREATE_ALONGSIDE
                else:
                    hook_mode = HookMode.CANCEL
                self._create_all_hooks(hook_path, hook_mode)

        else:
            self._print_gateway.print('Git not initialized in this directory.')

    def _create_all_hooks(self, hook_folder_path: str, hook_mode: HookMode):
        if hook_mode is not HookMode.CANCEL:
            create_hook(hook_folder_path, Hooks.PRE_COMMIT, hook_mode)
            create_hook(hook_folder_path, Hooks.POST_COMMIT, hook_mode)
            create_hook(hook_folder_path, Hooks.COMMIT_MSG, hook_mode)

    def help(self):
        pass

    @classmethod
    def get_short_help_message(cls):
        return 'Start guet usage in the repository at current directory'

    @classmethod
    def get_list_of_required_arguments_in_correct_order(cls):
        return cls._REQUIRED_ARGS_IN_CORRECT_ORDER
