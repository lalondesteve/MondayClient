import MondayClient.queries
from MondayClient.item import ItemCollection, Item
from MondayClient.base import MondayItem
import MondayClient.queries.utils as utils


class Board(MondayItem):
    # TODO: Query items by column values
    def __init__(self, data, client, collection, board_id=None, item_id=None):
        super().__init__(data, client)
        self.collection = collection
        self._items = None
        self._item = None
        if not data:
            if board_id and item_id:
                data = self.get_data(board_id, item_id)
            elif board_id:
                data = self.get_data(board_id)
            else:
                raise ValueError('data or board_id must be specified')
            self.data = data
        self.id = data['board_id']
        self.name = data['name']
        self.description = data["description"]
        if item_id:
            item = data["items"][0]
            self.item = item

    @property
    def items(self):
        if not self._items:
            r = self.client.execute_query(MondayClient.queries.get.items(self.id))
            try:
                _items = r["data"]["boards"][0].get("items")
            except Exception:
                raise
            else:
                self._items = ItemCollection(_items, self.client)
        return self._items

    @property
    def item(self):
        return self._item

    @item.setter
    def item(self, value):
        if not self._items and isinstance(value, dict):
            self._item = Item(value, self.client, None)
            return
        if isinstance(value, dict):
            value = value.get('item_id')
        elif isinstance(value, list) and len(value) == 1:
            value = value[0]
        self._item = self.items[value]

    def get_data(self, board_id, item_id=None):
        if item_id:
            r = self.client.execute_query(
                self.client.queries.get.board_and_item(board_id, item_id))
        else:
            r = self.client.execute_query(
                self.client.queries.get.board(board_id))
        return r["data"]["boards"][0]

    def refresh(self):
        self.client.board = None
        self.update_values()
        if self.collection:
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
