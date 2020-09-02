import json
from .utils import minify

"""update functions must always return two variables"""


def item_name(board: int, item_id: int, new_name: str):
    """
    Return query to update item's name

    :param board:
    :param item_id:
    :param new_name:
    :return: query, variables
    """
    return multiple_column_values(board, item_id, name=new_name)


def multiple_column_values(board_id: int, item_id: int, values=None, **kwargs):
    """
    Return query of type change_multiple_column_values

    :param board_id:
    :param item_id:
    :param values: dict of values or nothing
    :param kwargs: key value pair that will be used as values or nothing
    :return: query, variables
    """
    if values is None:
        values = {}
    values.update(kwargs)
    variables = {'column_values': json.dumps(values)}
    query = f"""mutation($column_values: JSON!){{
                change_multiple_column_values (
                    board_id: {board_id},
                    item_id: {item_id},
                    column_values: $column_values)
                {{id}}
            }}"""
    return minify(query), variables


def column_value(board_id: int, item_id: int, column_id: str, value):
    """
    Return a query to change a single column value

    :param board_id:
    :param item_id:
    :param column_id:
    :param value:
    :return: query, variables
    """
    if type(value) is not str:
        value = json.dumps(json.dumps(value))

    query = f'''mutation {{
                change_column_value(
                    board_id:{board_id},
                    item_id:{item_id},
                    column_id:{column_id},
                    value: {value})
                {{
                    id column_values (ids:{column_id}) {{id text}}
                }}
            }}'''
    return minify(query), None
