def validate_params_count(params, count):
    if len(params) != count:
        raise ValueError(
            f'Invalid number of arguments. Expected: {count}; received: {len(params)}.")')

def try_parse_float(s):
    try:
        return float(s)
    except:
        raise ValueError('Invalid value for weight. Should be a number.')

