from typing import Literal

SUFFIX_FILTERS_TYPE = {
    'int': {'gt', 'gte', 'lt', 'lte'},
    'str': {'icontains'},
} 

def make_param_filters(type:Literal['int', 'str'], param:str, include_itself=True, ignore=[]):
    filters = { f'{param}__{v}' for v in SUFFIX_FILTERS_TYPE[type] if v not in ignore }

    if include_itself:
        filters.add(param)

    return filters

def to_dto_or_msg_error(statuscode:int, msg:str, obj, iterable=False) -> dict | list:
    if statuscode == 200:
        return [o.to_dto() for o in obj] if iterable else obj.to_dto()
    return {'detail': msg}

def format_coin(val:float):
    return f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")