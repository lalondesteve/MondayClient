from MondayClient.base import MondayItem


class ItemColumns(MondayItem):
    def __init__(self, data, client, parent):
        super().__init__(data, client)
        self.columns = {x['column_id']: x for x in data}
        self.parent = parent

    def __iter__(self):
        yield from (self.columns.get(i) for i in self.columns)

    def __getitem__(self, key):
        key = self._get_partial_key(key)
        if 'text' in self.columns[key]:
            return self.columns[key]['text']
        else:
            return self.columns[key]['value']

    def __setitem__(self, key, value):
        key = self._get_partial_key(key)
        if 'text' in self.columns[key]:
            self.columns[key]['text'] = value
        else:
            self.columns[key]['value'] = value
        # TODO: update value via api

    def _get_partial_key(self, key):
        if key not in self.columns:
            if any(k.startswith(key) for k in self.columns):
                key = [k for k in self.columns if k.startswith(key)][0]
            else:
                raise KeyError(f'{key} not in {self.parent.name}')
        return key
