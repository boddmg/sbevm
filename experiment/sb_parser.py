__author__ = 'boddmg'
from texttable import *
from sb_lexer import Token
from sb_lexer import Lexer
import sb_lexer
from copy import deepcopy

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
    ['B', ['int', 'name', ';']],
    ['B', ['if', '(', 'E', ')', '{', 'B', '}', 'else', '{', 'B', '}']],
    ['B', ['A', ';']],

    ['A', ['V', '=', 'E']],

    ['E', ['T', 'Et']],

    ['Et', ['aop', 'T', 'Et']],
    ['Et', ['empty']],
    ['T', ['F', 'Tf']],
    ['Tf', ['mop', 'F', 'Tf']],
    ['Tf', ['empty']],
    ['F', ['(', 'E', ')']],
    ['F', ['V']],
    ['aop', ['+']],
    ['aop', ['-']],
    ['mop', ['*']],
    ['mop', ['/']],

    ['V', ['number']],
    ['V', ['name']],
]

class ParserException(Exception):
    pass

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
        first_set['empty'] = set(['empty'])

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

    # the table is table[terminal_symbol][non_terminal_symbol]
    def calculate_predict_table(self):
        predict_table = dict()
        for i in self._terminal_symbol:
            predict_table[i] = dict()
        predict_table['$'] = dict()

        first_set = self.first_set if self.first_set != None else self.calculate_first_set()
        follow_set = self.follow_set if self.follow_set != None else self.calculate_follow_set()

        for i in self._derivations:
            for j in self.get_sub_string_first_set(i[1]):
                if j in self._terminal_symbol:
                    if predict_table[j].has_key(i[0]):
                        print str([ j,i,predict_table[j][i[0]],self.get_sub_string_first_set(i[1]) ])
                        raise ParserException
                    predict_table[j][i[0]] = i
            if 'empty' in self.get_sub_string_first_set(i[1]):
                for j in follow_set[i[0]]:
                    if j in self._terminal_symbol:
                        #if i[1] == ['empty']:
                        #    continue
                        if predict_table[j].has_key(i[0]):
                            print str([ j,i,predict_table[j][i[0]],self.get_sub_string_first_set(i[1]) ])
                            raise ParserException
                        predict_table[j][i[0]] = i

        self._predict_table = predict_table
        return predict_table

    def build_the_ast(self, _source_lexer = Lexer()):
        try:
            ast_root = {}
            ast_stack = []
            symbol_stack = []
            number_stack = []
            program = _source_lexer
            predict_stack = ['$','S']
            X = predict_stack[-1]
            current_token = program.get_next_token()
            while True:
                if current_token.type_eq(X):
                    print 'terminal:',predict_stack.pop()
                    current_token = program.get_next_token()
                elif X in self._terminal_symbol:
                    print X,current_token
                    raise
                elif not self._predict_table[current_token._type].has_key(X):
                    print X,current_token
                    raise
                elif self._predict_table[current_token._type].has_key(X):
                    item = self._predict_table[current_token._type][X]
                    print item[0],'->',item[1]
                    item = item[1][:]
                    predict_stack.pop()
                    for i in range(len(item)):
                        new_item = item.pop()
                        if new_item != 'empty':
                            predict_stack.append(new_item)
                X = predict_stack[-1]
        except sb_lexer.LexerEmpty:
            pass
        print 'predict over'

        pass



def print_set_dict(set_dict):
    table = Texttable()
    table.header(['name', 'set'])
    for i in set_dict:
        table.add_row([i, str(set_dict[i])])
    print table.draw()

def print_2d_dict_table(table):
    row_header = table.keys()
    row_header.sort()
    col_header = set()
    for i in table:
        col_header |= set(table[i].keys())

    col_header = list(col_header)

    print_table = Texttable()
    print_table.header(['non terminal symbol'] + row_header)
    print_table.set_cols_width([10]*(len(row_header)+1))

    for y in col_header:
        new_row = [y]
        for x in row_header:
            new_item = '-'
            for j in table[x]:
                if y == table[x][j][0]:
                    new_item = table[x][j]
                    new_item = new_item[0] + '->' + ''.join(new_item[1])
            new_row.append(new_item)
        print_table.add_row(new_row)
    print print_table.draw()

    pass

if __name__ == "__main__":
    parser = Parser(derivations,terminal_symbol)
    first_set = parser.calculate_first_set()
    follow_set = parser.calculate_follow_set()
    non_terminal_symbol = parser.calculate_non_terminal_symbol()

    print_set_dict(dict(filter(lambda (k,v):k in non_terminal_symbol,first_set.items())))
    print_set_dict(dict(filter(lambda (k,v):k in non_terminal_symbol,follow_set.items())))
    print_2d_dict_table(parser.calculate_predict_table())
    parser.build_the_ast(Lexer("a=b+c+2*3;"))

