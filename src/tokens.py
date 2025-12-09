"""
MiniLang Token Definitions
토큰 타입과 토큰 클래스를 정의합니다.
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Any


class TokenType(Enum):
    """토큰 타입 열거형"""
    # 리터럴
    INTEGER = auto()        # 정수 리터럴
    FLOAT = auto()          # 실수 리터럴
    STRING = auto()         # 문자열 리터럴
    BOOLEAN = auto()        # 불리언 리터럴 (true, false)
    
    # 식별자
    IDENTIFIER = auto()     # 변수명, 함수명 등
    
    # 키워드
    LET = auto()            # let (변수 선언)
    IF = auto()             # if
    ELSE = auto()           # else
    WHILE = auto()          # while
    FOR = auto()            # for
    FUNC = auto()           # func (함수 정의)
    RETURN = auto()         # return
    PRINT = auto()          # print (내장 함수)
    INPUT = auto()          # input (내장 함수)
    TRUE = auto()           # true
    FALSE = auto()          # false
    NULL = auto()           # null
    BREAK = auto()          # break
    CONTINUE = auto()       # continue
    
    # 산술 연산자
    PLUS = auto()           # +
    MINUS = auto()          # -
    MULTIPLY = auto()       # *
    DIVIDE = auto()         # /
    MODULO = auto()         # %
    POWER = auto()          # **
    
    # 비교 연산자
    EQ = auto()             # ==
    NEQ = auto()            # !=
    LT = auto()             # <
    GT = auto()             # >
    LTE = auto()            # <=
    GTE = auto()            # >=
    
    # 논리 연산자
    AND = auto()            # and, &&
    OR = auto()             # or, ||
    NOT = auto()            # not, !
    
    # 대입 연산자
    ASSIGN = auto()         # =
    PLUS_ASSIGN = auto()    # +=
    MINUS_ASSIGN = auto()   # -=
    MULT_ASSIGN = auto()    # *=
    DIV_ASSIGN = auto()     # /=
    
    # 구분자
    LPAREN = auto()         # (
    RPAREN = auto()         # )
    LBRACE = auto()         # {
    RBRACE = auto()         # }
    LBRACKET = auto()       # [
    RBRACKET = auto()       # ]
    COMMA = auto()          # ,
    SEMICOLON = auto()      # ;
    COLON = auto()          # :
    
    # 특수
    EOF = auto()            # 파일 끝
    NEWLINE = auto()        # 줄바꿈


@dataclass
class Token:
    """토큰 클래스"""
    type: TokenType
    value: Any
    line: int
    column: int
    
    def __repr__(self):
        return f"Token({self.type.name}, {repr(self.value)}, line={self.line}, col={self.column})"


# 키워드 매핑
KEYWORDS = {
    'let': TokenType.LET,
    'if': TokenType.IF,
    'else': TokenType.ELSE,
    'while': TokenType.WHILE,
    'for': TokenType.FOR,
    'func': TokenType.FUNC,
    'return': TokenType.RETURN,
    'print': TokenType.PRINT,
    'input': TokenType.INPUT,
    'true': TokenType.TRUE,
    'false': TokenType.FALSE,
    'null': TokenType.NULL,
    'and': TokenType.AND,
    'or': TokenType.OR,
    'not': TokenType.NOT,
    'break': TokenType.BREAK,
    'continue': TokenType.CONTINUE,
}

# 연산자 매핑 (길이 순으로 정렬 - 긴 것 먼저)
OPERATORS = {
    '**': TokenType.POWER,
    '==': TokenType.EQ,
    '!=': TokenType.NEQ,
    '<=': TokenType.LTE,
    '>=': TokenType.GTE,
    '&&': TokenType.AND,
    '||': TokenType.OR,
    '+=': TokenType.PLUS_ASSIGN,
    '-=': TokenType.MINUS_ASSIGN,
    '*=': TokenType.MULT_ASSIGN,
    '/=': TokenType.DIV_ASSIGN,
    '+': TokenType.PLUS,
    '-': TokenType.MINUS,
    '*': TokenType.MULTIPLY,
    '/': TokenType.DIVIDE,
    '%': TokenType.MODULO,
    '<': TokenType.LT,
    '>': TokenType.GT,
    '=': TokenType.ASSIGN,
    '!': TokenType.NOT,
}

# 구분자 매핑
DELIMITERS = {
    '(': TokenType.LPAREN,
    ')': TokenType.RPAREN,
    '{': TokenType.LBRACE,
    '}': TokenType.RBRACE,
    '[': TokenType.LBRACKET,
    ']': TokenType.RBRACKET,
    ',': TokenType.COMMA,
    ';': TokenType.SEMICOLON,
    ':': TokenType.COLON,
}
