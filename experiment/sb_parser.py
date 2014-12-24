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

class Parser():
    def __init__(self,_derivation,_terminal_symbol):
        self.derivation = _derivation
        self.terminal_symbol = _terminal_symbol
        self.first_set = None
        self.follow_set = None

    def calculate_first_set(self):
        non_terminal_symbol = set([x[0] for x in derivations])
        first_set = dict()
        for i in terminal_symbol:
            first_set[i] = {i}
        for i in non_terminal_symbol:
            first_set[i] = set()

        for i in self.derivation:
            if i[1] == ['empty']:
                first_set[i[0]].add('empty')
                continue

        while True:
            last_set = str(first_set)
            for i in self.derivation:
                for j in i[1]:
                    if j == 'empty':
                        break
                    current_symbol = first_set[j]
                    first_set[i[0]] = first_set[i[0]] | (current_symbol-{"empty"})
                    if 'empty' not in first_set[j]:
                        break
            if str(first_set) == last_set:
                break
        self.first_set = first_set
        return first_set

    def calculate_follow_set(self):



        pass


if __name__ == "__main__":
    parser = Parser(derivations,terminal_symbol)
    first_set = parser.calculate_first_set()
    table = Texttable()
    table.header(['name','set'])
    non_terminal_symbol = set([x[0] for x in derivations])
    for i in first_set:
        if i in non_terminal_symbol:
            table.add_row([i,str(first_set[i])])
    print table.draw()

