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
    ['S', ['P']],
    ['S', ['empty']],
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
    def __init__(self,derivation,terminal_symbol):
        self._derivations = derivation
        self._terminal_symbol = terminal_symbol
        self.first_set = None
        self.follow_set = None

    def calculate_non_terminal_symbol(self):
        self._non_terminal_symbol = set([x[0] for x in derivations])
        self._non_terminal_symbol.add('S')
        return self._non_terminal_symbol

    def calculate_first_set(self):
        non_terminal_symbol = self.calculate_non_terminal_symbol()
        first_set = dict()
        for i in terminal_symbol:
            first_set[i] = {i}
        for i in non_terminal_symbol:
            first_set[i] = set()

        for i in self._derivations:
            if i[1] == ['empty']:
                first_set[i[0]].add('empty')
                continue

        while True:
            last_set_hash = str(first_set)
            for i in self._derivations:
                for j in i[1]:
                    if j == 'empty':
                        break
                    current_symbol = first_set[j]
                    first_set[i[0]] |= (current_symbol-{"empty"})
                    if 'empty' not in first_set[j]:
                        break
            if str(first_set) == last_set_hash:
                break
        self.first_set = first_set
        return first_set

    def calculate_follow_set(self):
        follow_set = {'S':{'$'}}
        non_terminal_symbol = self.calculate_non_terminal_symbol()
        for i in non_terminal_symbol | terminal_symbol:
            follow_set[i] = set()

        derivations = self._derivations
        while True:
            last_follow_hash = str(follow_set)
            for i in derivations:
                for j in range(len(i[1])):
                    if j < len(i[1])-1 :
                        
                        follow_set[i[1][j]] |= self.first_set[i[1][j+1]] - {'empty'}
                    if j == len(i[1])-1 :
                        follow_set[i[1][j]] |= follow_set[i[0]]

            if last_follow_hash == str(follow_set):
                break
        self._follow_set = follow_set
        return follow_set

def print_set_dict(set_dict):
    table = Texttable()
    table.header(['name', 'set'])
    for i in set_dict:
        table.add_row([i, str(set_dict[i])])
    print table.draw()


if __name__ == "__main__":
    parser = Parser(derivations,terminal_symbol)
    first_set = parser.calculate_first_set()
    follow_set = parser.calculate_follow_set()
    non_terminal_symbol = parser.calculate_non_terminal_symbol()

    print_set_dict(dict(filter(lambda (k,v):k in non_terminal_symbol,first_set.items())))
    print_set_dict(dict(filter(lambda (k,v):k in non_terminal_symbol,follow_set.items())))

