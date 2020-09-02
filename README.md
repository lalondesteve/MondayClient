# MondayClient
A client to query Monday.com v2 API

### Requirements
- Python > 3.6
- requests
- python-dotenv

### Getting Started
This code uses python-dotenv to set environment variables
You will need a .env file with your monday api key as a variable:
`MONDAY_TOKEN="{{API TOKEN}}"`

### Query and access Example
```
import MondayClient
mc = MondayClient.Client()
print(mc.boards.values)

mc.board = {{board_id}}
print(mc.board.items.values)

mc.board.item = {{item_id}}
print(mc.board.item.columns.values)

print(mc.board.item.columns['{{column_id}}'])
```

Only basic implementation of mutation for certain column types are implemented

### Mutation example
```
import MondayClient
mc = MondayClient.Client()
mc.board = {{board_id}}
mc.board.item = {{item_id}}
mc.board.item.columns['status'] = value

mc.board.item.update_multiple_columns(status=value1, note=value2)
# OR
values = {status: value1, note: value2)
mc.board.item.update_multiple_columns(values=values)
```

Implemented column types :

| GUI name | (API type) |
| :------: | :--------: |
| Checkbox | (boolean)  |
| Status   | (color)    | 
| Dropdown | (dropdown) | 
| Text     | (text)     | 
| Date     | (date)     | 
