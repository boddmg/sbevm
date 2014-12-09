import unittest
import sb_lexer

class test_lexer(unittest.TestCase):
    def test_keyword(self):
       lexer = sb_lexer.Lexer(" int function")
       self.assertEqual(lexer.get_next_token(),sb_lexer.Token("int","int"))
       self.assertEqual(lexer.get_next_token(),sb_lexer.Token("function","function"))
