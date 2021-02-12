class Args(list):

    def __init__(self, raw_args):
        super().__init__()
        self._raw_args = raw_args

    def __setitem__(self, index, data):
        self._raw_args[index] = data

    def __getitem__(self, index):
        return self._raw_args[index]

    def __len__(self):
        return len(self._raw_args)

    @property
    def without_flags(self):
        new_args = []
        for arg in self._raw_args:
            if not arg.startswith('-'):
                new_args.append(arg)
        return new_args
