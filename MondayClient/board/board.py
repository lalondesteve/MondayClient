import MondayClient.queries
from MondayClient.item import ItemCollection
from MondayClient.base import MondayItem


class Board(MondayItem):
    def __init__(self, data, client, collection):
        super().__init__(data, client)
        self.collection = collection
        self.id = data['board_id']
        self.name = data['name']
        self.updated_at = data["updated_at"]
        self.description = data["description"]
        self._items = None
        self._item = None

    @property
    def items(self):
        if not self._items:
            r = self.client.execute_query(MondayClient.queries.get.items(self.id))
            try:
                self._items = r["data"]["boards"][0].get("items")
            except Exception as e:
                print(r, e)
            else:
                self._items = ItemCollection(self._items, self.client)
        return self._items

    @property
    def item(self):
        return self._item

    @item.setter
    def item(self, value):
        if type(value) is dict:
            value = value.get('item_id')
        elif type(value) is list and len(value) == 1:
            value = value[0]
        self._item = self.items[value]

    # TODO: Query items by column values

    def refresh(self):
        self.client.board = None
        self.update_values()
        self.collection.update_board(self.id, self.values)
        self.client.board = self.id

    def update_values(self):
        r = self.client.execute_query(
            self.client.queries.get.board(self.id))
        self.values = r["data"]["boards"][0]

    def get_items_by_column_value(self, column_id, value):
        r = self.client.execute_query(
            self.client.queries.get.items_by_column_value(
                self.id, column_id, value
            )
        )
        return r["data"]["items_by_column_values"]
