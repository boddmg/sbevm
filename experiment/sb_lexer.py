__author__ = 'boddmg'

import re

class UnkownToken(Exception):
    pass

class UnkownLexerError(Exception):
    pass

class LexerEmpty(Exception):
    pass

regex_table=[
    # Keyword
    ["int", "int"],
    ["if", "if"],
    ["else", "else"],
    ["while", "while"],

    # lex
    ["number", "[0-9]+"],
    ["name", "[A-Za-z_]+[\w]*"],

    #symbol
    ["!=", "!="],
    ["==", "=="],
    [":", ":"],
    [">=", "\>\="],
    ["<=", "\<\="],
    [">", "\>"],
    ["<", "\<"],
    ["+", "\+"],
    ["-", "\-"],
    ["*", "\*"],
    ["\\", "\\\\"],
    ["=", "="],
    ["(", "\("],
    [")", "\)"],
    ["{", "\{"],
    ["}", "\}"],
    [";", ";"]

]

class Token():
    def __init__(self,_type,_content=""):
        self._type = _type
        self._content = _content
        self._source = _content

    def type_eq(self, symbol):
        return self._type == symbol

    def __eq__(self, other):
        if self._content != other._content:
            return False
        if self._type != other._type:
            return False
        return True

    def __ne__(self, other):
       return not self.__eq__(other)

    def __str__(self):
        return "type: %s , content: %s" % (self._type,self._content)

class Lexer():
    def __init__(self,_source_text=""):
        self._source_text = _source_text
        #self._pattern = re.compile()

    def get_next_token(self):
        self._source_text = self._source_text.lstrip()
        if self._source_text.strip() == "":
            raise LexerEmpty

        try:
            for regex_pair in regex_table:
                regex = "\\A"+regex_pair[1]
                match = re.match(regex,self._source_text)
                if match:
                    new_token = Token(regex_pair[0],match.group(0))
                    self._source_text=self._source_text[match.end(0):]
                    return new_token
            raise UnkownToken
        except UnkownToken:
            print self._source_text
            raise
        except:
            raise UnkownLexerError


