def minify(_str):
    return ' '.join(_str.split())


def get_value_from_key(key, values):
    if hasattr(values, 'items'):
        for k, v in values.items():
            if k == key:
                yield v
            if isinstance(v, dict):
                yield from get_value_from_key(key, v)
            elif isinstance(v, list):
                for i in v:
                    yield from get_value_from_key(key, i)


def get_key_from_value(value, values):
    if hasattr(values, 'items'):
        for k, v in values.items():
            if v == value:
                yield k
            if isinstance(v, dict):
                yield from get_key_from_value(value, v)
            elif isinstance(v, list):
                for i in v:
                    yield from get_key_from_value(value, i)