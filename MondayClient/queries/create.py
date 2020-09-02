def new_item(board_id, name):
    query = f"""{{ create_item(
        boards(ids:{board_id}){{
            item_name: {name} )
                {{id}}
        }}
    }}"""
    return query
