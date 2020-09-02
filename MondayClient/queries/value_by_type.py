
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
