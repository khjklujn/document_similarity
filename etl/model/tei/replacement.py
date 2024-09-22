from unicodedata import normalize


replacement_with_space = (
    '`', '1', '2', '3', '4', '5', '6', '7',
    '8', '9', '0', '=', '[', ']', ';',
    "'", ',', '.', '/', '~', '@', '#', '$',
    '$', '%', '^', '&', '*', '(', ')', '_',
    '+', '{', '}', ':', '"', '<', '>', '?',
    '\\', '|', '\t', '\n', '\r',
)


def down_encode(text: str) -> str:
    return normalize(
        'NFKD',
        text.strip()
    ).encode('ascii', 'ignore').decode('ascii')


def replace(text: str) -> str:
    ret = text
    for char in replacement_with_space:
        ret = ret.replace(char, ' ')
    return ret


def scrub(text: str) -> str:
    ret = replace(text).strip()
    return ' '.join(
        [
            word.lower().replace('null', '-null-').replace('-', '')
            for word in ret.split(' ')
            if len(word) > 1
        ]
    )
