from .tools import make_param_filters

REGISTRIES_FILTERS = make_param_filters('int', 'value') | make_param_filters('str', 'title') | {'status', 'type_in', 'occurrance_init', 'occurrance_end', 'date_ref'}
MONTHS = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
