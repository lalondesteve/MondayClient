from MondayClient.base import MondayItem
from MondayClient.exceptions import MondayAPIError


class ItemColumns(MondayItem):
    def __init__(self, data, client, parent):
        super().__init__(data, client)
        self.columns = {x['column_id']: x for x in data}
        self.parent = parent

    def __iter__(self):
        yield from (self.columns.get(i) for i in self.columns)

    def __getitem__(self, key):
        key = self._get_from_partial_key_or_title(key)
        if 'text' in self.columns[key]:
            return self.columns[key]['text']
        else:
            return self.columns[key]['value']

    def __setitem__(self, key, value):
        item = self._get_col_from_key(key)
        print("item", item)
        if 'text' in item:
            item['text'] = value

        item['value'] = value
        self._update_column(item)

    def _get_from_partial_key_or_title(self, key):
        if key not in self.columns:
            # if exact key is not available, search for partial key or title
            if any(k.startswith(key) for k in self.columns):
                keys = [k for k in self.columns if k.startswith(key)]
            elif any(k['title'].lower().startswith(key.lower()) for k in self.values):
                keys = [k['column_id'] for k in self.values if k['title'].lower().startswith(key.lower())]
            else:
                raise KeyError(f'{key} not in {self.parent.name}')
            if len(keys) > 1:
                raise KeyError(f'{key} pattern could match multiple column ids or title {keys}')
            else:
                key = keys[0]
        return key

    def _get_col_from_key(self, key):
        key = self._get_from_partial_key_or_title(key)
        return self.columns[key]

    def _update_column(self, item):
        v = self.client.queries.get.value_by_column_type(item['type'], item['value'])
        r = self.client.execute_query(
            *self.client.queries.update.column_value(
                self.client.board.id, self.parent.id, item['column_id'], v))
        if 'error_code' in r:
            raise MondayAPIError(r)

    def update_multiple_columns(self, values=None, **kwargs):
        if not values:
            values = {}
        if kwargs:
            values.update(kwargs)
        values_to_send = {}
        for k, v in values.items():
            if k == 'name':
                values_to_send['name'] = v
                continue
            col = self._get_col_from_key(k)
            value = self.client.queries.get.value_by_column_type(col['type'], v)
            values_to_send.update({col['column_id']: value})
        r = self.client.execute_query(
            *self.client.queries.update.multiple_column_values(
                self.client.board.id,
                self.parent.id,
                values=values_to_send
            )
        )
        if 'error_code' in r:
            raise MondayAPIError(r)
        return r
