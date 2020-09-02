class MondayCollection:
    def __init__(self, client):
        self.client = client
        self.collection = {}

    def __iter__(self):
        yield from (self.collection.get(i) for i in self.collection)

    def __len__(self):
        return len(self.collection)

    def __getitem__(self, item_id):
        item = self.collection.get(str(item_id))
        if item is None:
            raise KeyError(f'ID {item_id} not in collection')
        return item

    @property
    def values(self):
        return [self.collection[x].values for x in self.collection]
        # yield from (self.collection[x].values for x in self.collection)


class MondayItem:
    def __init__(self, data, client):
        self.client = client
        self.values = data
        self.type = type(self)

    # def __setattr__(self, key, value):
    #     object.__setattr__(self, key, value)
