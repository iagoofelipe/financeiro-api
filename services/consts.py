from .tools import make_param_filters

REGISTRIES_FILTERS = make_param_filters('int', 'value') | make_param_filters('str', 'title') | {'status', 'type_in', 'occurrance_init', 'occurrance_end', 'date_ref'}