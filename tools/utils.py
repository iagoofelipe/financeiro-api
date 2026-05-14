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