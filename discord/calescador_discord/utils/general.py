def filter_not_none(d: dict) -> dict:
    return {k: v for k, v in d.items() if v != None}

def map_noneable(value, f):
    return f(value) if value != None else None
