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
    non_terminal_symbol = set([x[0] for x in derivations])
    first_set = dict()
    for i in terminal_symbol:
        first_set[i] = {i}
    for i in non_terminal_symbol:
        first_set[i] = set()

    for i in derivation:
        if i[1] == ['empty']:
            first_set[i[0]].add('empty')
            continue

    while True:
        last_set = first_set
        for i in derivation:
            for j in i[1]:
                if 'empty' not in first_set[j]:
                    break
                current_symbol = first_set[i[1]]
                first_set[i[0]] = first_set[i[0]] | current_symbol.remove("empty")
        if first_set == last_set:
            break
    pass

class Parser():
    def __init__(self):
        pass

if __name__ == "__main__":
    print get_first_set(derivations)