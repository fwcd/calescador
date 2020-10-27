def filter_not_none(d: dict) -> dict:
    return {k: v for k, v in d.items() if v != None}
