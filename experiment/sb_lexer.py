__author__ = 'boddmg'

import re

regex_table={
    # Keyword
    "int" : "int",
    "function" : "function",

    # lex
    "name" : "[A-Za-z_]+[\w]",

    #symbol
    ":" : ":",
    "+" : "+",
    "-" : "-",
    "*" : "*",
    "\\" : "\\",
    "{" : "{",
    "}" : "}",
    ";" : ";"

}

class Token():
    def __init__(self,_type,_content=""):
        self._type = _type
        self._content = _content
        self._source = _content

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
        self._source_text = self._source_text.lstrip(" ")

        for key in regex_table:
            match = re.match("\\A"+regex_table[key],self._source_text)
            if match:
                new_token = Token(key,match.group(0))
                self._source_text=self._source_text[match.end(0):]
                return new_token


