import unittest
import sb_lexer
import sb_parser

sample_program = '''
int a=0;
a = 1+1-1*1\\1;
'''

sample_tokens = [
    sb_lexer.Token("int","int"),
    sb_lexer.Token("name","a"),
    sb_lexer.Token("=","="),
    sb_lexer.Token("number","0"),
    sb_lexer.Token(";",";"),
    sb_lexer.Token("name","a"),
    sb_lexer.Token("=","="),
    sb_lexer.Token("number","1"),
    sb_lexer.Token("+","+"),
    sb_lexer.Token("number","1"),
    sb_lexer.Token("-","-"),
    sb_lexer.Token("number","1"),
    sb_lexer.Token("*","*"),
    sb_lexer.Token("number","1"),
    sb_lexer.Token("\\","\\"),
    sb_lexer.Token("number","1"),
    sb_lexer.Token(";",";"),
]

class test_parser(unittest.TestCase):
    def test_token_flow(self):
        lexer = sb_lexer.Lexer(sample_program)
        current_token = None
        for i in range(len(sample_tokens)):
            try:
                current_token = lexer.get_next_token()
                self.assertEqual(sample_tokens[i],current_token)
            except:
                print i,"sample:",sample_tokens[i],"  token:",current_token
                raise

    def test_the_ast(self):
        pass

    def test_the_predict_table(self):

        terminal_symbol = {
        'id',
        '+',
        '*',
        '(',
        ')',
        '$'
        }

        derivations = [
            ['S',['E']],
            ['E', ['T', 'E`']],
            ['E`', ['+', 'T', 'E`']],
            ['E`', ['empty']],
            ['T', ['F', 'T`']],
            ['T`', ['empty']],
            ['T`', ['*', 'F', 'T`']],
            ['F', ['(', 'E', ')']],
            ['F', ['id']],
        ]


        parser = sb_parser.Parser(derivations,terminal_symbol)
        non_terminal_symbol = parser.calculate_non_terminal_symbol()
        first_set = parser.calculate_first_set()
        follow_set = parser.calculate_follow_set()
        predict_table = parser.calculate_predict_table()

        try:
            self.assertEqual(first_set['F'],first_set['T'])
            self.assertEqual(first_set['T'],first_set['E'])
            self.assertEqual(first_set['E'],{'(','id'})
            self.assertEqual(first_set['E`'],{'+','empty'})
            self.assertEqual(first_set['T`'],{'*','empty'})
        except:
            sb_parser.print_set_dict(dict(filter(lambda (k,v):k in non_terminal_symbol,first_set.items())))
            raise

        try:
            self.assertEqual(follow_set['E'], {')','$'})
            self.assertEqual(follow_set['E`'],{')','$'})
            self.assertEqual(follow_set['T'], {'+',')','$'})
            self.assertEqual(follow_set['T`'],{'+',')','$'})
            self.assertEqual(follow_set['F'],{'+','*',')','$'})
        except:
            sb_parser.print_set_dict(dict(filter(lambda (k,v):k in non_terminal_symbol,follow_set.items())))
            raise

        try:
            self.assertEqual(predict_table['id']['E'],['E',['T','E`']])
            self.assertEqual(predict_table['id']['T'],['T',['F','T`']])
            self.assertEqual(predict_table['id']['F'],['F',['id']])
            self.assertEqual(predict_table['+']['E`'],['E`',['+','T','E`']])
            self.assertEqual(predict_table['+']['T`'],['T`',['empty']])
            self.assertEqual(predict_table['*']['T`'],['T`',['*','F','T`']])
            self.assertEqual(predict_table['(']['E'],['E',['T','E`']])
            self.assertEqual(predict_table['(']['T'],['T',['F','T`']])
            self.assertEqual(predict_table['(']['F'],['F',['(','E',')']])
            self.assertEqual(predict_table[')']['E`'],['E`',['empty']])
            self.assertEqual(predict_table[')']['T`'],['T`',['empty']])
            self.assertEqual(predict_table['$']['E`'],['E`',['empty']])
            self.assertEqual(predict_table['$']['T`'],['T`',['empty']])
        except:
            sb_parser.print_2d_dict_table(predict_table)
            raise
        pass






