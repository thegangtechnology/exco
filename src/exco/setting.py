import re

start_cell_marker = '{{--'
start_table_marker = '{{--table'
start_col_marker = '{{--col'
end_marker = '--}}'

default_locator = 'at_comment_cell'

# keys:

k_key = 'key'
k_name = 'name'
k_parser = 'parser'
k_params = 'params'
k_locator = 'locator'
k_validations = 'validations'
k_assumptions = 'assumptions'
k_fallback = 'fallback'
k_table_key = 'table_key'
k_columns = 'columns'
k_end_conditions = 'end_conditions'
k_item_direction = 'item_direction'

table_infinite_loop_guard = 10000

# Note should I make another none like singleton for this?
default_fallback_value = None

# deref pattern
spec_to_extractor_deref_re = re.compile(r'==([A-Z]{1,3}\d+)==')
template_to_spec_deref_re = re.compile(r'<<([A-Z]{1,3}\d+)>>')
