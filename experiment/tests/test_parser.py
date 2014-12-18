import unittest
import sb_lexer

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

