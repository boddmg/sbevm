__author__ = 'boddmg'

terminal_symbol = {
    'number',
    'name',
    'int',
    'if',
    '+',
    '-',
    '*',
    '/',
    '=',
    '(',
    ')',
    '{',
    '}',
    'while',
    '$'
}

derivations = [
    ['P', ['B', 'P']],
    ['P', ['empty']],
    ['B', ['int', 'E']],
    ['B', ['if', '(', 'E', '{', 'B', '}', 'else', '{', 'B', '}']],
    ['B', ['E', ';']],
    ['B', ['empty']],
    ['E', ['V', 'Ev']],
    ['E', ['(', 'E', ')', 'E`']],
    ['Ev', ['empty']],
    ['Ev', ['=', 'E']],
    ['Ev', ['E`']],
    ['E`', ['+', 'E`']],
    ['E`', ['-', 'E`']],
    ['E`', ['*', 'E`']],
    ['E`', ['/', 'E`']],
    ['E`', ['empty']],
    ['V', ['number']],
    ['V', ['name']],
]

non_terminal_symbol = set([x[0] for x in derivations])


def get_first_set(derivation):
    first_set = {}
    for i in non_terminal_symbol|terminal_symbol:
        first_set[i] = {}
    for i in derivation:
        if i[1][0] in terminal_symbol:
            first_set[i] = i
            continue




    pass

class Parser():
    def __init__(self):
        pass