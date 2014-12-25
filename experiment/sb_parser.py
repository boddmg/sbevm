__author__ = 'boddmg'
from texttable import *

terminal_symbol = {
    'number',
    'name',
    'int',
    'if',
    'else',
    '+',
    '-',
    '*',
    '/',
    '=',
    '(',
    ')',
    '{',
    '}',
    ';',
    'while',
    '$'
}

derivations = [
    ['S', ['P']],
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
        non_terminal_symbol = set([x[0] for x in self._derivations])
        non_terminal_symbol.add('S')
        return non_terminal_symbol

    def calculate_first_set(self):
        non_terminal_symbol = self.calculate_non_terminal_symbol()
        first_set = dict()
        for i in self._terminal_symbol:
            first_set[i] = {i}
        for i in non_terminal_symbol:
            first_set[i] = set()

        for i in self._derivations:
            if i[1][0] == 'empty':
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

    def get_sub_string_first_set(self,sub_string):
        first_set = set()
        for i in sub_string:
            first_set |= self.first_set[i]
            if 'empty' not in self.first_set[i]:
                first_set -= {'empty'}
                return first_set
        return first_set

    def calculate_follow_set(self):
        follow_set = dict()
        non_terminal_symbol = self.calculate_non_terminal_symbol()
        for i in non_terminal_symbol | self._terminal_symbol:
            follow_set[i] = set()

        follow_set['S']={'$'}

        derivations = self._derivations
        while True:
            last_follow = follow_set.copy()
            for i in derivations:
                for j in range(len(i[1])):

                    if i[1][j] == 'empty':
                        break

                    if j < len(i[1])-1 :
                        follow_set[i[1][j]] = follow_set[i[1][j]] | self.get_sub_string_first_set(i[1][j+1:]) - {'empty'}
                        #print 'origin:',i[1],j,i[1][j+1:],self.get_sub_string_first_set(i[1][j+1:]),follow_set[i[1][j]],i[1][j]

                    if j == len(i[1])-1 or ('empty' in self.get_sub_string_first_set(i[1][j+1:])) :
                        #print 'added:',i[0],i[1],i[1][j],j,follow_set[i[0]],follow_set[i[1][j]]
                        follow_set[i[1][j]] = follow_set[i[1][j]] | follow_set[i[0]]

            if last_follow == follow_set:
                break
        self._follow_set = follow_set
        return follow_set

    def calculate_predict_table(self):
        first_set = self.first_set
        follow_set = self.follow_set

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

