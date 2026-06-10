from .tools import make_param_filters

REGISTRY_FILTERS = make_param_filters('int', 'value') | make_param_filters('str', 'title') | {'status', 'type_in', 'occurrance_init', 'occurrance_end', 'date_ref'}
CARD_FILTERS = set()
INVOICE_FILTERS = { 'card_id' }