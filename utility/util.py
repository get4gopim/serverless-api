import re


def index_of(original_string, search_string):
    delimiter_idx = -1

    try:
        delimiter_idx = original_string.index(search_string)
    except ValueError:
        delimiter_idx = -1

    return delimiter_idx;


def is_uuid(location):
    pattern = '[0-9a-f]{64}\Z'
    return re.match(pattern, location)