

def verify_user_data(data, keys_to_verify):
    """verifies that a list of keys exist in the JSON data and :returns a list of missing keys"""
    missing_kays = []

    # verify JSON data
    for key in keys_to_verify:
        try:
            data[key]
        except KeyError:
            missing_kays.append(key)

    return missing_kays

    