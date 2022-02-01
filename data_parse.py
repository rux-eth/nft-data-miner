def parse_data(data: dict) -> dict:
    token_id = data['token_id']
    result = {
        "token_id": token_id
    }
    for trait in data['traits']:
        result[trait['trait_type']] = trait['value']
    return result

def get_keys(list_of_dicts) -> list:
    temp = []
    for elem in list_of_dicts:
        for key in elem:
            if not key in temp:
                temp.append(key)
    return temp