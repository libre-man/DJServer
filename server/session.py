class SimpleSessionstore(dict):
    def __init__(self):
        self.__setitem__(0, SimpleSession())


class SimpleSession():
    def __init__(self, name="CoolDisco"):
        self.name = name

    @property
    def channels(self):
        return [{"channel_id": 1,
                 "color": "red",
                 "url": "http://test.test"},
                {"channel_id": 2,
                 "color": "blue",
                 "url": "http://test2.test"}]
