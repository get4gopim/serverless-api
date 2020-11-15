import re


def index_of(original_string, search_string):
    delimiter_idx = -1

    try:
        delimiter_idx = original_string.index(search_string)
    except ValueError:
        delimiter_idx = -1

    return delimiter_idx;


def get_str_after(original_string, find_str):
    mod_str = ''
    idx = index_of(original_string, find_str)
    if idx > 0:
        mod_str = original_string[0:idx]
    return mod_str


def is_uuid(location):
    pattern = '[0-9a-f]{64}\Z'
    return re.match(pattern, location)