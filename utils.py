from tonsdk.utils import Address


def convert_address(address: str):
    return Address(address).to_string(True, True, False, False)


def join_with_limit(list: list, limit: int = 200):
    text = ''
    for item in list:
        text += f'{item}, '
        if len(text) > limit:
            return text[:-2] + ', ...'
    return text[:-2]
