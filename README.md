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

### Example
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

Mutation queries are not implemented yet. 

