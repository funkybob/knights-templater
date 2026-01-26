
_js_escapes = str.maketrans(
    {
        '\\': '\\u005C',
        "'": '\\u0027',
        '"': '\\u0022',
        '>': '\\u003E',
        '<': '\\u003C',
        '&': '\\u0026',
        '=': '\\u003D',
        '-': '\\u002D',
        ';': '\\u003B',
        '\u2028': '\\u2028',
        '\u2029': '\\u2029',
    },
)

# Escape every ASCII character with a value less than 32.
_js_escapes.update((z, f'\\u{z:04X}') for z in range(32))


def escape_js(text: str) -> str:
    return text.translate(_js_escapes)
