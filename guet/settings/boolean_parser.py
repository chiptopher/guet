
def boolean_parser(value: str) -> bool:
    valid_trues = ['True', 'true']
    valid_falses = ['False', 'false']
    if value in valid_trues:
        return True
    elif value in valid_falses:
        return False
    else:
        raise AttributeError
