from MondayClient.item import Item
from MondayClient.base import MondayCollection


class ItemCollection(MondayCollection):
    def __init__(self, items, client):
        super().__init__(client)
        self.collection = {item['item_id']: Item(item, client, self)
                           for item in items}

    def update_item(self, item_id, item):
        self.collection[item_id] = Item(item, self.client, self)
