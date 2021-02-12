class Proxy:
    def __init__(self, proxy_object=None):
        self.proxy_object = proxy_object

    def __getattribute__(self, name):
        # This won't load self.proxy_object if it's a propery that's accessed.

        if name == 'proxy_object':
            return object.__getattribute__(self, 'proxy_object')
        if name == 'loader':
            return object.__getattribute__(self, 'loader')
        if self.proxy_object is None:
            self.proxy_object = self.loader()
        return getattr(self.proxy_object, name)

    def loader(self):
        raise NotImplementedError
