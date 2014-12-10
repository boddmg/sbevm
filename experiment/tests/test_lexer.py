import unittest
import sb_lexer


class test_lexer(unittest.TestCase):
    def test_keyword(self):
       lexer = sb_lexer.Lexer(" int function")
       self.assertEqual(lexer.get_next_token(),sb_lexer.Token("int","int"))
       self.assertEqual(lexer.get_next_token(),sb_lexer.Token("function","function"))

    def test_expression(self):
        lexer = sb_lexer.Lexer("  int  _abc = 123 +1 *2-3; \n b = 123 + 12;")
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

