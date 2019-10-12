from os.path import join

from guet.git._hook_mode import HookMode


class _HookCreateStrategy:

    def __init__(self, hook_folder_path: str, create_mode: HookMode):
        self.create_mode = create_mode
        self.hook_folder_path = hook_folder_path

    def final_hook_path(self):
        return join(self.hook_folder_path, self.create_mode(self.name()))

    def name(self) -> str:
        raise NotImplementedError

    def file_lines(self) -> [str]:
        raise NotImplementedError
