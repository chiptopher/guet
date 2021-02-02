class Proxy:
    def __init__(self, proxy_object=None):
        self.proxy_object = proxy_object

    def __getattribute__(self, name):
        # TODO handle @attribute.setter correctly. Right now if you try and do
        # a GitProxy.commit_msg = 'something' it won't actually load the real
        # Git object

        if name == 'proxy_object':
            return object.__getattribute__(self, 'proxy_object')
        if name == 'loader':
            return object.__getattribute__(self, 'loader')
        if self.proxy_object is None:
            self.proxy_object = self.loader()
        return getattr(self.proxy_object, name)

    def loader(self):
        raise NotImplementedError
