import string

ALL_CHAR = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя ' + string.ascii_lowercase + string.digits

def translate_url(text):
    table = (('а', 'a'),
             ('б', 'b'),
             ('в', 'v'),
             ('г', 'g'),
             ('д', 'd'),
             ('е', 'e'),
             ('ё', 'yo'),
             ('ж', 'zh'),
             ('з', 'z'),
             ('и', 'i'),
             ('й', 'j'),
             ('к', 'k'),
             ('л', 'l'),
             ('м', 'm'),
             ('н', 'n'),
             ('о', 'o'),
             ('п', 'p'),
             ('р', 'r'),
             ('с', 's'),
             ('т', 't'),
             ('у', 'u'),
             ('ф', 'f'),
             ('х', 'h'),
             ('ц', 'c'),
             ('ч', 'ch'),
             ('ш', 'sh'),
             ('щ', 'shch'),
             ('ъ', ''),
             ('ы', 'y'),
             ('ь', ''),
             ('э', 'eh'),
             ('ю', 'yu'),
             ('я', 'ya'),
             (' ', '-'))

    text = text.lower()

    text = ' '.join(''.join([x for x in text if x in ALL_CHAR]).split())

    for i, j in table:
        text = text.replace(i, j)

    return text