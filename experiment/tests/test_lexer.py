import unittest
import sb_lexer

sample_program = '''
int a = 10;
int b;
int c;
c=a*b;

if(a==1)
{
c=1;
}else
{
    c=0;
}
while(a<=10)
{
a=a+1;
}
'''

sample_tokens = [
    sb_lexer.Token("int","int"),
    sb_lexer.Token("name","a"),
    sb_lexer.Token("=","="),
    sb_lexer.Token("number","10"),
    sb_lexer.Token(";",";"),
    sb_lexer.Token("int","int"),
    sb_lexer.Token("name","b"),
    sb_lexer.Token(";",";"),
    sb_lexer.Token("int","int"),
    sb_lexer.Token("name","c"),
    sb_lexer.Token(";",";"),
    sb_lexer.Token("name","c"),
    sb_lexer.Token("=","="),
    sb_lexer.Token("name","a"),
    sb_lexer.Token("*","*"),
    sb_lexer.Token("name","b"),
    sb_lexer.Token(";",";"),
    sb_lexer.Token("if","if"),
    sb_lexer.Token("(","("),
    sb_lexer.Token("name","a"),
    sb_lexer.Token("==","=="),
    sb_lexer.Token("number","1"),
    sb_lexer.Token(")",")"),
    sb_lexer.Token("{","{"),
    sb_lexer.Token("name","c"),
    sb_lexer.Token("=","="),
    sb_lexer.Token("number","1"),
    sb_lexer.Token(";",";"),
    sb_lexer.Token("}","}"),
    sb_lexer.Token("else","else"),
    sb_lexer.Token("{","{"),
    sb_lexer.Token("name","c"),
    sb_lexer.Token("=","="),
    sb_lexer.Token("number","0"),
    sb_lexer.Token(";",";"),
    sb_lexer.Token("}","}"),

    sb_lexer.Token("while","while"),
    sb_lexer.Token("(","("),
    sb_lexer.Token("name","a"),
    sb_lexer.Token("<=","<="),
    sb_lexer.Token("number","10"),
    sb_lexer.Token(")",")"),
    sb_lexer.Token("{","{"),
    sb_lexer.Token("name","a"),
    sb_lexer.Token("=","="),
    sb_lexer.Token("name","a"),
    sb_lexer.Token("+","+"),
    sb_lexer.Token("number","1"),
    sb_lexer.Token(";",";"),
    sb_lexer.Token("}","}"),
]

class test_lexer(unittest.TestCase):
    def test_symbol(self):
       lexer = sb_lexer.Lexer(" + - * \\ > < >= <= == != = (){};")
       self.assertEqual(lexer.get_next_token(),sb_lexer.Token("+","+"))
       self.assertEqual(lexer.get_next_token(),sb_lexer.Token("-","-"))
       self.assertEqual(lexer.get_next_token(),sb_lexer.Token("*","*"))
       self.assertEqual(lexer.get_next_token(),sb_lexer.Token("\\","\\"))
       self.assertEqual(lexer.get_next_token(),sb_lexer.Token(">",">"))
       self.assertEqual(lexer.get_next_token(),sb_lexer.Token("<","<"))
       self.assertEqual(lexer.get_next_token(),sb_lexer.Token(">=",">="))
       self.assertEqual(lexer.get_next_token(),sb_lexer.Token("<=","<="))
       self.assertEqual(lexer.get_next_token(),sb_lexer.Token("==","=="))
       self.assertEqual(lexer.get_next_token(),sb_lexer.Token("!=","!="))
       self.assertEqual(lexer.get_next_token(),sb_lexer.Token("=","="))
       self.assertEqual(lexer.get_next_token(),sb_lexer.Token("(","("))
       self.assertEqual(lexer.get_next_token(),sb_lexer.Token(")",")"))
       self.assertEqual(lexer.get_next_token(),sb_lexer.Token("{","{"))
       self.assertEqual(lexer.get_next_token(),sb_lexer.Token("}","}"))
       self.assertEqual(lexer.get_next_token(),sb_lexer.Token(";",";"))

    def test_keyword(self):
       lexer = sb_lexer.Lexer(" int if else while ")
       self.assertEqual(lexer.get_next_token(),sb_lexer.Token("int","int"))
       self.assertEqual(lexer.get_next_token(),sb_lexer.Token("if","if"))
       self.assertEqual(lexer.get_next_token(),sb_lexer.Token("else","else"))
       self.assertEqual(lexer.get_next_token(),sb_lexer.Token("while","while"))

    def test_expression(self):
        lexer = sb_lexer.Lexer("  int  _abc = 123 +1 *2-3; \n b = 123 + 12;")
        try:
            self.assertEqual(lexer.get_next_token(),sb_lexer.Token("int","int"))
            self.assertEqual(lexer.get_next_token(),sb_lexer.Token("name","_abc"))
            self.assertEqual(lexer.get_next_token(),sb_lexer.Token("=","="))
            self.assertEqual(lexer.get_next_token(),sb_lexer.Token("number","123"))
            self.assertEqual(lexer.get_next_token(),sb_lexer.Token("+","+"))
            self.assertEqual(lexer.get_next_token(),sb_lexer.Token("number","1"))
            self.assertEqual(lexer.get_next_token(),sb_lexer.Token("*","*"))
            self.assertEqual(lexer.get_next_token(),sb_lexer.Token("number","2"))
            self.assertEqual(lexer.get_next_token(),sb_lexer.Token("-","-"))
            self.assertEqual(lexer.get_next_token(),sb_lexer.Token("number","3"))
            self.assertEqual(lexer.get_next_token(),sb_lexer.Token(";",";"))
            self.assertEqual(lexer.get_next_token(),sb_lexer.Token("name","b"))
            self.assertEqual(lexer.get_next_token(),sb_lexer.Token("=","="))
            self.assertEqual(lexer.get_next_token(),sb_lexer.Token("number","123"))
            self.assertEqual(lexer.get_next_token(),sb_lexer.Token("+","+"))
            self.assertEqual(lexer.get_next_token(),sb_lexer.Token("number","12"))
            self.assertEqual(lexer.get_next_token(),sb_lexer.Token(";",";"))
        except:
            raise

    def test_program(self):
        lexer = sb_lexer.Lexer(sample_program)
        current_token = None
        for i in range(len(sample_tokens)):
            try:
                current_token = lexer.get_next_token()
                self.assertEqual(sample_tokens[i],current_token)
            except:
                print i,"sample:",sample_tokens[i],"  token:",current_token
                raise

