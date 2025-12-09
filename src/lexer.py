"""
MiniLang Lexer (어휘 분석기)
소스 코드를 토큰 스트림으로 변환합니다.
"""

from typing import List, Optional
from tokens import Token, TokenType, KEYWORDS, OPERATORS, DELIMITERS


class LexerError(Exception):
    """렉서 에러 클래스"""
    def __init__(self, message: str, line: int, column: int):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Lexer Error at line {line}, column {column}: {message}")


class Lexer:
    """어휘 분석기 클래스"""
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
    
    @property
    def current_char(self) -> Optional[str]:
        """현재 문자 반환"""
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]
    
    def peek(self, offset: int = 1) -> Optional[str]:
        """다음 문자 미리보기"""
        pos = self.pos + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]
    
    def advance(self) -> Optional[str]:
        """다음 문자로 이동"""
        char = self.current_char
        self.pos += 1
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char
    
    def skip_whitespace(self):
        """공백 건너뛰기 (줄바꿈 제외)"""
        while self.current_char and self.current_char in ' \t\r':
            self.advance()
    
    def skip_comment(self):
        """주석 건너뛰기"""
        # 단일 행 주석: // 또는 #
        if self.current_char == '/' and self.peek() == '/':
            while self.current_char and self.current_char != '\n':
                self.advance()
            return True
        
        if self.current_char == '#':
            while self.current_char and self.current_char != '\n':
                self.advance()
            return True
        
        # 다중 행 주석: /* ... */
        if self.current_char == '/' and self.peek() == '*':
            start_line = self.line
            start_col = self.column
            self.advance()  # /
            self.advance()  # *
            
            while self.current_char:
                if self.current_char == '*' and self.peek() == '/':
                    self.advance()  # *
                    self.advance()  # /
                    return True
                self.advance()
            
            raise LexerError("Unterminated multi-line comment", start_line, start_col)
        
        return False
    
    def read_number(self) -> Token:
        """숫자 리터럴 읽기"""
        start_line = self.line
        start_col = self.column
        num_str = ''
        has_dot = False
        
        while self.current_char and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                if has_dot:
                    break
                if not (self.peek() and self.peek().isdigit()):
                    break
                has_dot = True
            num_str += self.advance()
        
        if has_dot:
            return Token(TokenType.FLOAT, float(num_str), start_line, start_col)
        else:
            return Token(TokenType.INTEGER, int(num_str), start_line, start_col)
    
    def read_string(self) -> Token:
        """문자열 리터럴 읽기"""
        start_line = self.line
        start_col = self.column
        quote_char = self.advance()  # ' 또는 "
        string_value = ''
        
        while self.current_char and self.current_char != quote_char:
            if self.current_char == '\\':
                self.advance()
                escape_char = self.current_char
                if escape_char == 'n':
                    string_value += '\n'
                elif escape_char == 't':
                    string_value += '\t'
                elif escape_char == 'r':
                    string_value += '\r'
                elif escape_char == '\\':
                    string_value += '\\'
                elif escape_char == quote_char:
                    string_value += quote_char
                else:
                    string_value += '\\' + (escape_char or '')
                if self.current_char:
                    self.advance()
            elif self.current_char == '\n':
                raise LexerError("Unterminated string literal", start_line, start_col)
            else:
                string_value += self.advance()
        
        if not self.current_char:
            raise LexerError("Unterminated string literal", start_line, start_col)
        
        self.advance()  # 닫는 따옴표
        return Token(TokenType.STRING, string_value, start_line, start_col)
    
    def read_identifier(self) -> Token:
        """식별자 또는 키워드 읽기"""
        start_line = self.line
        start_col = self.column
        ident = ''
        
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            ident += self.advance()
        
        # 키워드 확인
        token_type = KEYWORDS.get(ident)
        if token_type:
            if token_type == TokenType.TRUE:
                return Token(TokenType.BOOLEAN, True, start_line, start_col)
            elif token_type == TokenType.FALSE:
                return Token(TokenType.BOOLEAN, False, start_line, start_col)
            return Token(token_type, ident, start_line, start_col)
        
        return Token(TokenType.IDENTIFIER, ident, start_line, start_col)
    
    def read_operator(self) -> Optional[Token]:
        """연산자 읽기"""
        start_line = self.line
        start_col = self.column
        
        # 길이가 긴 연산자부터 확인 (2글자)
        if self.current_char and self.peek():
            two_char = self.current_char + self.peek()
            if two_char in OPERATORS:
                self.advance()
                self.advance()
                return Token(OPERATORS[two_char], two_char, start_line, start_col)
        
        # 1글자 연산자
        if self.current_char in OPERATORS:
            char = self.advance()
            return Token(OPERATORS[char], char, start_line, start_col)
        
        return None
    
    def tokenize(self) -> List[Token]:
        """소스 코드를 토큰화"""
        self.tokens = []
        
        while self.current_char:
            # 공백 건너뛰기
            self.skip_whitespace()
            
            if not self.current_char:
                break
            
            # 주석 건너뛰기
            if self.skip_comment():
                continue
            
            # 줄바꿈
            if self.current_char == '\n':
                # 줄바꿈은 선택적으로 토큰화 (세미콜론 대신 사용 가능)
                line, col = self.line, self.column
                self.advance()
                # 연속된 빈 줄은 하나로 처리
                if self.tokens and self.tokens[-1].type != TokenType.NEWLINE:
                    self.tokens.append(Token(TokenType.NEWLINE, '\\n', line, col))
                continue
            
            # 숫자
            if self.current_char.isdigit():
                self.tokens.append(self.read_number())
                continue
            
            # 문자열
            if self.current_char in '"\'':
                self.tokens.append(self.read_string())
                continue
            
            # 식별자/키워드
            if self.current_char.isalpha() or self.current_char == '_':
                self.tokens.append(self.read_identifier())
                continue
            
            # 구분자
            if self.current_char in DELIMITERS:
                line, col = self.line, self.column
                char = self.advance()
                self.tokens.append(Token(DELIMITERS[char], char, line, col))
                continue
            
            # 연산자
            op_token = self.read_operator()
            if op_token:
                self.tokens.append(op_token)
                continue
            
            # 알 수 없는 문자
            raise LexerError(f"Unexpected character: '{self.current_char}'", self.line, self.column)
        
        # EOF 토큰 추가
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        
        return self.tokens


def tokenize(source: str) -> List[Token]:
    """편의 함수: 소스 코드를 토큰화"""
    lexer = Lexer(source)
    return lexer.tokenize()


if __name__ == "__main__":
    # 테스트
    test_code = '''
    // 변수 선언 테스트
    let x = 10
    let y = 20.5
    let name = "Hello, World!"
    
    /* 다중 행 주석
       테스트 */
    
    # 조건문 테스트
    if x > 5 {
        print(x + y)
    }
    
    // 함수 정의
    func add(a, b) {
        return a + b
    }
    '''
    
    try:
        tokens = tokenize(test_code)
        for token in tokens:
            print(token)
    except LexerError as e:
        print(f"Error: {e}")
