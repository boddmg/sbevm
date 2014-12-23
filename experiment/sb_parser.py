__author__ = 'boddmg'

from texttable import *

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
    derivation = filter(lambda x:x[1]!=['empty'], derivation)
    while True:
        last_set = str(first_set)
        for i in derivation:
            for j in i[1]:
                print i,j
                for symbol in first_set[j]:
                    first_set[i[0]].add(symbol)

                if 'empty' not in first_set[j]:
                    break
        if str(first_set) == last_set:
            break
    return first_set

def get_follow_set(derivation):

    pass

class Parser():
    def __init__(self):
        pass

if __name__ == "__main__":
    table = Texttable()
    first_set = get_first_set(derivations)
    table.header(['name','first set'])
    for i in non_terminal_symbol:
        row = [i,str(first_set[i])]
        table.add_row(row)
    print table.draw()