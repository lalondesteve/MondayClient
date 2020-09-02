from .utils import minify
import json


def boards(limit=1000):
    return f"{{boards(limit:{limit}){{" \
           f"board_id:id name description updated_at}} }}"


def board(board_id):
    return f"{{boards(ids:{board_id}){{" \
           f"board_id:id name description updated_at}} }}"


def items(board_id):
    query = f"""{{
        boards(ids:{board_id}){{
            items {{item_id:id name}}
        }}
    }}"""
    return minify(query)


def item(item_id):
    return f"{{items(ids:{item_id}){{" \
           f"item_id:id name}} }}"


def columns(item_id=None, board_id=None):
    if item_id:
        qry_header = f'items(ids:{item_id})'
    elif board_id:
        qry_header = f'boards(ids:{board_id}'
    else:
        raise TypeError('Either item_id or board_id must be specified')
    return f"""{{ {qry_header} {{column_values{{id type}} }} }}"""


def column_value(item_id, columns_ids, values=None):
    if values is None:
        values = 'id value text'
    elif values == 'all':
        values = 'id text title type value'
    if ' id' in values:
        values = values.replace(' id', 'column_id:id')
    elif values.find('id') == 0:
        values = values.replace('id', 'column_id:id')
    columns_ids = json.dumps(columns_ids)
    query = f"""{{
        items(ids:{item_id}){{
            item_id:id name
            column_values(ids:{columns_ids}){{
                {values}
            }}
        }}
    }}"""
    return minify(query)


def value_by_column_type(column_type, value):
    if column_type == 'boolean':
        if value is True:
            return {"checked": "true"}
        elif value is False:
            return {}

    if column_type == "color":
        return {"label": f"{value}"}

    if column_type == "dropdown":
        return {"labels": [f"{value}"]}

    if column_type == "text":
        return f"{value}"

    if column_type == "date":
        # when should we check the validity of date?
        return {"date": "{value"}
