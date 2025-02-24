from errors.application_error import ApplicationError


def validate_params_count(params, count):
    if len(params) != count:
        raise ApplicationError(f"Invalid number of arguments. Expected: {count} / Received: {len(params)}.")

def validate_unknown_params_count(params, min_count, max_count):
    if min_count > len(params) or len(params) > max_count:
        raise ApplicationError(f"Invalid number of arguments. Expected at least {min_count},"
                               f" not more than {max_count} / Received: {len(params)}.")

def try_parse_float(s):
    try:
        return float(s)
    except:
        raise ApplicationError("Invalid value. Should be a number.")

def try_parse_int(s):
    try:
        return int(s)
    except:
        raise ApplicationError("Invalid value. Should be a number.")
