import MondayClient.queries
from MondayClient.base import MondayItem
from .item_columns import ItemColumns


class Item(MondayItem):
    def __init__(self, data, client, collection, columns=None):
        super().__init__(data, client)
        self.collection = collection
        self._columns = None
        self.id = data['item_id']
        self._name = data['name']
        self.updated_at = data['updated_at']
        self._columns_ids = columns
        if 'column_values' in data:
            self.columns = data['column_values']

    @property
    def columns_ids(self):
        if not self._columns_ids:
            r = self.client.execute_query(
                MondayClient.queries.get.columns(
                    item_id=self.id))
            values = r["data"]["items"][0]["column_values"]
            self._columns_ids = [x["id"] for x in values]
        return self._columns_ids

    @property
    def columns(self):
        if not self._columns:
            r = self.client.execute_query(
                MondayClient.queries.get.column_value(
                    self.id, self._columns, values='all'))
            values = r["data"]["items"][0]["column_values"]
            self._columns = ItemColumns(values, self.client, self)
        return self._columns

    @columns.setter
    def columns(self, value):
        self._columns = ItemColumns(value, self.client, self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        r = self.client.execute_query(
            MondayClient.queries.update.item_name(
                self.client.board.id, self.id, value
            )
        )
        self._name = value

    def refresh(self):
        self.client.board.item = None
        self.update_values()
        self.collection.update_item(self.id, self.values)
        self.client.board.item = self.id

    def update_values(self):
        r = self.client.execute_query(
            self.client.queries.get.item(self.id))
        self.values = r["data"]["items"][0]

    def update_multiple_columns(self, values=None, **kwargs):
        self.columns.update_multiple_columns(values=values, **kwargs)
        # self.refresh()
