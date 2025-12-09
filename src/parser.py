"""
MiniLang Parser (구문 분석기)
토큰 스트림을 AST(추상 구문 트리)로 변환합니다.
재귀 하강 파서(Recursive Descent Parser) 방식으로 구현합니다.
"""

from typing import List, Optional, Callable
from tokens import Token, TokenType
from ast_nodes import *


class ParseError(Exception):
    """파서 에러 클래스"""
    def __init__(self, message: str, token: Token):
        self.message = message
        self.token = token
        super().__init__(f"Parse Error at line {token.line}, column {token.column}: {message}")


class Parser:
    """구문 분석기 클래스"""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.errors: List[ParseError] = []
    
    @property
    def current(self) -> Token:
        """현재 토큰"""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]  # EOF
    
    @property
    def previous(self) -> Token:
        """이전 토큰"""
        if self.pos > 0:
            return self.tokens[self.pos - 1]
        return self.tokens[0]
    
    def peek(self, offset: int = 1) -> Token:
        """다음 토큰 미리보기"""
        pos = self.pos + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return self.tokens[-1]
    
    def is_at_end(self) -> bool:
        """파일 끝 여부"""
        return self.current.type == TokenType.EOF
    
    def check(self, *types: TokenType) -> bool:
        """현재 토큰 타입 확인"""
        return self.current.type in types
    
    def advance(self) -> Token:
        """다음 토큰으로 이동"""
        if not self.is_at_end():
            self.pos += 1
        return self.previous
    
    def match(self, *types: TokenType) -> bool:
        """토큰 타입이 일치하면 소비"""
        if self.check(*types):
            self.advance()
            return True
        return False
    
    def consume(self, token_type: TokenType, message: str) -> Token:
        """특정 토큰 타입 소비 (없으면 에러)"""
        if self.check(token_type):
            return self.advance()
        raise ParseError(message, self.current)
    
    def skip_newlines(self):
        """줄바꿈 건너뛰기"""
        while self.match(TokenType.NEWLINE):
            pass
    
    def synchronize(self):
        """에러 복구: 다음 문장 시작점으로 이동"""
        self.advance()
        
        while not self.is_at_end():
            if self.previous.type in (TokenType.SEMICOLON, TokenType.NEWLINE):
                return
            
            if self.current.type in (
                TokenType.LET,
                TokenType.FUNC,
                TokenType.IF,
                TokenType.WHILE,
                TokenType.FOR,
                TokenType.RETURN,
                TokenType.PRINT,
            ):
                return
            
            self.advance()
    
    # =====================================================
    # 파싱 메서드들
    # =====================================================
    
    def parse(self) -> Program:
        """프로그램 파싱"""
        statements = []
        
        self.skip_newlines()
        
        while not self.is_at_end():
            try:
                stmt = self.parse_declaration()
                if stmt:
                    statements.append(stmt)
            except ParseError as e:
                self.errors.append(e)
                self.synchronize()
            
            self.skip_newlines()
        
        return Program(statements=statements, line=1, column=1)
    
    def parse_declaration(self) -> Optional[Statement]:
        """선언문 파싱"""
        if self.match(TokenType.LET):
            return self.parse_variable_declaration()
        if self.match(TokenType.FUNC):
            return self.parse_function_declaration()
        return self.parse_statement()
    
    def parse_variable_declaration(self) -> VariableDeclaration:
        """변수 선언 파싱: let name = expression"""
        name_token = self.consume(TokenType.IDENTIFIER, "Expected variable name")
        name = name_token.value
        
        initializer = None
        if self.match(TokenType.ASSIGN):
            initializer = self.parse_expression()
        
        self.consume_statement_terminator()
        
        return VariableDeclaration(
            name=name,
            initializer=initializer,
            line=name_token.line,
            column=name_token.column
        )
    
    def parse_function_declaration(self) -> FunctionDeclaration:
        """함수 선언 파싱: func name(params) { body }"""
        name_token = self.consume(TokenType.IDENTIFIER, "Expected function name")
        name = name_token.value
        
        self.consume(TokenType.LPAREN, "Expected '(' after function name")
        
        parameters = []
        if not self.check(TokenType.RPAREN):
            parameters.append(self.consume(TokenType.IDENTIFIER, "Expected parameter name").value)
            while self.match(TokenType.COMMA):
                parameters.append(self.consume(TokenType.IDENTIFIER, "Expected parameter name").value)
        
        self.consume(TokenType.RPAREN, "Expected ')' after parameters")
        
        self.skip_newlines()
        self.consume(TokenType.LBRACE, "Expected '{' before function body")
        
        body = self.parse_block()
        
        return FunctionDeclaration(
            name=name,
            parameters=parameters,
            body=body,
            line=name_token.line,
            column=name_token.column
        )
    
    def parse_statement(self) -> Statement:
        """문장 파싱"""
        if self.match(TokenType.IF):
            return self.parse_if_statement()
        if self.match(TokenType.WHILE):
            return self.parse_while_statement()
        if self.match(TokenType.FOR):
            return self.parse_for_statement()
        if self.match(TokenType.RETURN):
            return self.parse_return_statement()
        if self.match(TokenType.BREAK):
            return self.parse_break_statement()
        if self.match(TokenType.CONTINUE):
            return self.parse_continue_statement()
        if self.match(TokenType.PRINT):
            return self.parse_print_statement()
        if self.match(TokenType.LBRACE):
            return self.parse_block()
        
        return self.parse_expression_statement()
    
    def parse_if_statement(self) -> IfStatement:
        """조건문 파싱: if condition { then } else { else }"""
        token = self.previous
        
        # 조건 (괄호 선택적)
        has_paren = self.match(TokenType.LPAREN)
        condition = self.parse_expression()
        if has_paren:
            self.consume(TokenType.RPAREN, "Expected ')' after if condition")
        
        self.skip_newlines()
        self.consume(TokenType.LBRACE, "Expected '{' after if condition")
        then_branch = self.parse_block()
        
        else_branch = None
        self.skip_newlines()
        if self.match(TokenType.ELSE):
            self.skip_newlines()
            if self.match(TokenType.IF):
                else_branch = self.parse_if_statement()
            else:
                self.consume(TokenType.LBRACE, "Expected '{' after 'else'")
                else_branch = self.parse_block()
        
        return IfStatement(
            condition=condition,
            then_branch=then_branch,
            else_branch=else_branch,
            line=token.line,
            column=token.column
        )
    
    def parse_while_statement(self) -> WhileStatement:
        """While 반복문 파싱: while condition { body }"""
        token = self.previous
        
        has_paren = self.match(TokenType.LPAREN)
        condition = self.parse_expression()
        if has_paren:
            self.consume(TokenType.RPAREN, "Expected ')' after while condition")
        
        self.skip_newlines()
        self.consume(TokenType.LBRACE, "Expected '{' after while condition")
        body = self.parse_block()
        
        return WhileStatement(
            condition=condition,
            body=body,
            line=token.line,
            column=token.column
        )
    
    def parse_for_statement(self) -> ForStatement:
        """For 반복문 파싱: for init; cond; incr { body }"""
        token = self.previous
        
        has_paren = self.match(TokenType.LPAREN)
        
        # 초기화
        initializer = None
        if self.match(TokenType.SEMICOLON):
            pass
        elif self.match(TokenType.LET):
            initializer = self.parse_variable_declaration_no_terminator()
            self.consume(TokenType.SEMICOLON, "Expected ';' after for initializer")
        else:
            initializer = ExpressionStatement(
                expression=self.parse_expression(),
                line=self.current.line,
                column=self.current.column
            )
            self.consume(TokenType.SEMICOLON, "Expected ';' after for initializer")
        
        # 조건
        condition = None
        if not self.check(TokenType.SEMICOLON):
            condition = self.parse_expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after for condition")
        
        # 증감
        increment = None
        if has_paren:
            if not self.check(TokenType.RPAREN):
                increment = self.parse_expression()
            self.consume(TokenType.RPAREN, "Expected ')' after for clauses")
        else:
            if not self.check(TokenType.LBRACE) and not self.check(TokenType.NEWLINE):
                increment = self.parse_expression()
        
        self.skip_newlines()
        self.consume(TokenType.LBRACE, "Expected '{' after for clauses")
        body = self.parse_block()
        
        return ForStatement(
            initializer=initializer,
            condition=condition,
            increment=increment,
            body=body,
            line=token.line,
            column=token.column
        )
    
    def parse_variable_declaration_no_terminator(self) -> VariableDeclaration:
        """변수 선언 파싱 (종결자 없이)"""
        name_token = self.consume(TokenType.IDENTIFIER, "Expected variable name")
        name = name_token.value
        
        initializer = None
        if self.match(TokenType.ASSIGN):
            initializer = self.parse_expression()
        
        return VariableDeclaration(
            name=name,
            initializer=initializer,
            line=name_token.line,
            column=name_token.column
        )
    
    def parse_return_statement(self) -> ReturnStatement:
        """Return 문 파싱"""
        token = self.previous
        
        value = None
        if not self.check(TokenType.SEMICOLON, TokenType.NEWLINE, TokenType.RBRACE, TokenType.EOF):
            value = self.parse_expression()
        
        self.consume_statement_terminator()
        
        return ReturnStatement(value=value, line=token.line, column=token.column)
    
    def parse_break_statement(self) -> BreakStatement:
        """Break 문 파싱"""
        token = self.previous
        self.consume_statement_terminator()
        return BreakStatement(line=token.line, column=token.column)
    
    def parse_continue_statement(self) -> ContinueStatement:
        """Continue 문 파싱"""
        token = self.previous
        self.consume_statement_terminator()
        return ContinueStatement(line=token.line, column=token.column)
    
    def parse_print_statement(self) -> PrintStatement:
        """Print 문 파싱: print(args)"""
        token = self.previous
        
        self.consume(TokenType.LPAREN, "Expected '(' after 'print'")
        
        arguments = []
        if not self.check(TokenType.RPAREN):
            arguments.append(self.parse_expression())
            while self.match(TokenType.COMMA):
                arguments.append(self.parse_expression())
        
        self.consume(TokenType.RPAREN, "Expected ')' after print arguments")
        self.consume_statement_terminator()
        
        return PrintStatement(arguments=arguments, line=token.line, column=token.column)
    
    def parse_block(self) -> Block:
        """블록 파싱: { statements }"""
        token = self.previous
        statements = []
        
        self.skip_newlines()
        
        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            stmt = self.parse_declaration()
            if stmt:
                statements.append(stmt)
            self.skip_newlines()
        
        self.consume(TokenType.RBRACE, "Expected '}' after block")
        
        return Block(statements=statements, line=token.line, column=token.column)
    
    def parse_expression_statement(self) -> ExpressionStatement:
        """표현식 문장 파싱"""
        expr = self.parse_expression()
        self.consume_statement_terminator()
        return ExpressionStatement(expression=expr, line=expr.line, column=expr.column)
    
    def consume_statement_terminator(self):
        """문장 종결자 소비 (; 또는 줄바꿈)"""
        if not self.match(TokenType.SEMICOLON, TokenType.NEWLINE):
            if not self.check(TokenType.RBRACE, TokenType.EOF):
                # 에러는 발생시키지 않고 경고만 (관대한 파싱)
                pass
    
    # =====================================================
    # 표현식 파싱 (연산자 우선순위에 따라)
    # =====================================================
    
    def parse_expression(self) -> Expression:
        """표현식 파싱"""
        return self.parse_assignment_expr()
    
    def parse_assignment_expr(self) -> Expression:
        """대입 표현식 파싱"""
        expr = self.parse_or_expr()
        
        if self.match(TokenType.ASSIGN, TokenType.PLUS_ASSIGN, TokenType.MINUS_ASSIGN,
                      TokenType.MULT_ASSIGN, TokenType.DIV_ASSIGN):
            operator = self.previous.value
            value = self.parse_assignment_expr()
            
            if isinstance(expr, Identifier):
                return Assignment(
                    target=expr,
                    operator=operator,
                    value=value,
                    line=expr.line,
                    column=expr.column
                )
            
            # 배열 인덱스 대입 지원
            if isinstance(expr, ArrayAccess):
                return ArrayIndexAssignment(
                    array=expr.array,
                    index=expr.index,
                    operator=operator,
                    value=value,
                    line=expr.line,
                    column=expr.column
                )
            
            raise ParseError("Invalid assignment target", self.previous)
        
        return expr
    
    def parse_or_expr(self) -> Expression:
        """OR 논리 연산"""
        expr = self.parse_and_expr()
        
        while self.match(TokenType.OR):
            operator = self.previous.value
            right = self.parse_and_expr()
            expr = BinaryOp(left=expr, operator='or', right=right, line=expr.line, column=expr.column)
        
        return expr
    
    def parse_and_expr(self) -> Expression:
        """AND 논리 연산"""
        expr = self.parse_equality_expr()
        
        while self.match(TokenType.AND):
            operator = self.previous.value
            right = self.parse_equality_expr()
            expr = BinaryOp(left=expr, operator='and', right=right, line=expr.line, column=expr.column)
        
        return expr
    
    def parse_equality_expr(self) -> Expression:
        """등호 비교 연산"""
        expr = self.parse_comparison_expr()
        
        while self.match(TokenType.EQ, TokenType.NEQ):
            operator = self.previous.value
            right = self.parse_comparison_expr()
            expr = BinaryOp(left=expr, operator=operator, right=right, line=expr.line, column=expr.column)
        
        return expr
    
    def parse_comparison_expr(self) -> Expression:
        """비교 연산"""
        expr = self.parse_additive_expr()
        
        while self.match(TokenType.LT, TokenType.GT, TokenType.LTE, TokenType.GTE):
            operator = self.previous.value
            right = self.parse_additive_expr()
            expr = BinaryOp(left=expr, operator=operator, right=right, line=expr.line, column=expr.column)
        
        return expr
    
    def parse_additive_expr(self) -> Expression:
        """덧셈/뺄셈 연산"""
        expr = self.parse_multiplicative_expr()
        
        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.previous.value
            right = self.parse_multiplicative_expr()
            expr = BinaryOp(left=expr, operator=operator, right=right, line=expr.line, column=expr.column)
        
        return expr
    
    def parse_multiplicative_expr(self) -> Expression:
        """곱셈/나눗셈/나머지 연산"""
        expr = self.parse_power_expr()
        
        while self.match(TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            operator = self.previous.value
            right = self.parse_power_expr()
            expr = BinaryOp(left=expr, operator=operator, right=right, line=expr.line, column=expr.column)
        
        return expr
    
    def parse_power_expr(self) -> Expression:
        """거듭제곱 연산 (우결합)"""
        expr = self.parse_unary_expr()
        
        if self.match(TokenType.POWER):
            operator = self.previous.value
            right = self.parse_power_expr()  # 우결합이므로 재귀 호출
            expr = BinaryOp(left=expr, operator=operator, right=right, line=expr.line, column=expr.column)
        
        return expr
    
    def parse_unary_expr(self) -> Expression:
        """단항 연산"""
        if self.match(TokenType.NOT, TokenType.MINUS):
            operator = self.previous.value
            if operator == '!':
                operator = 'not'
            operand = self.parse_unary_expr()
            return UnaryOp(
                operator=operator,
                operand=operand,
                line=self.previous.line,
                column=self.previous.column
            )
        
        return self.parse_postfix_expr()
    
    def parse_postfix_expr(self) -> Expression:
        """후위 연산 (함수 호출, 배열 접근)"""
        expr = self.parse_primary_expr()
        
        while True:
            if self.match(TokenType.LPAREN):
                # 함수 호출
                expr = self.finish_call(expr)
            elif self.match(TokenType.LBRACKET):
                # 배열 접근
                index = self.parse_expression()
                self.consume(TokenType.RBRACKET, "Expected ']' after index")
                expr = ArrayAccess(array=expr, index=index, line=expr.line, column=expr.column)
            else:
                break
        
        return expr
    
    def finish_call(self, callee: Expression) -> FunctionCall:
        """함수 호출 완성"""
        arguments = []
        
        if not self.check(TokenType.RPAREN):
            arguments.append(self.parse_expression())
            while self.match(TokenType.COMMA):
                arguments.append(self.parse_expression())
        
        self.consume(TokenType.RPAREN, "Expected ')' after function arguments")
        
        if isinstance(callee, Identifier):
            return FunctionCall(
                name=callee.name,
                arguments=arguments,
                line=callee.line,
                column=callee.column
            )
        
        raise ParseError("Can only call functions", self.previous)
    
    def parse_primary_expr(self) -> Expression:
        """기본 표현식"""
        # 숫자 리터럴
        if self.match(TokenType.INTEGER, TokenType.FLOAT):
            return NumberLiteral(
                value=self.previous.value,
                line=self.previous.line,
                column=self.previous.column
            )
        
        # 문자열 리터럴
        if self.match(TokenType.STRING):
            return StringLiteral(
                value=self.previous.value,
                line=self.previous.line,
                column=self.previous.column
            )
        
        # 불리언 리터럴
        if self.match(TokenType.BOOLEAN):
            return BooleanLiteral(
                value=self.previous.value,
                line=self.previous.line,
                column=self.previous.column
            )
        
        # Null 리터럴
        if self.match(TokenType.NULL):
            return NullLiteral(line=self.previous.line, column=self.previous.column)
        
        # 식별자
        if self.match(TokenType.IDENTIFIER):
            return Identifier(
                name=self.previous.value,
                line=self.previous.line,
                column=self.previous.column
            )
        
        # 괄호 표현식
        if self.match(TokenType.LPAREN):
            expr = self.parse_expression()
            self.consume(TokenType.RPAREN, "Expected ')' after expression")
            return expr
        
        # 배열 리터럴
        if self.match(TokenType.LBRACKET):
            elements = []
            if not self.check(TokenType.RBRACKET):
                elements.append(self.parse_expression())
                while self.match(TokenType.COMMA):
                    elements.append(self.parse_expression())
            self.consume(TokenType.RBRACKET, "Expected ']' after array elements")
            return ArrayLiteral(
                elements=elements,
                line=self.previous.line,
                column=self.previous.column
            )
        
        # input() 함수 (내장)
        if self.match(TokenType.INPUT):
            self.consume(TokenType.LPAREN, "Expected '(' after 'input'")
            prompt = None
            if not self.check(TokenType.RPAREN):
                prompt = self.parse_expression()
            self.consume(TokenType.RPAREN, "Expected ')' after input")
            args = [prompt] if prompt else []
            return FunctionCall(
                name='input',
                arguments=args,
                line=self.previous.line,
                column=self.previous.column
            )
        
        raise ParseError(f"Unexpected token: {self.current.type.name}", self.current)


def parse(tokens: List[Token]) -> Program:
    """편의 함수: 토큰 리스트를 파싱"""
    parser = Parser(tokens)
    program = parser.parse()
    
    if parser.errors:
        for error in parser.errors:
            print(f"Error: {error}")
    
    return program


if __name__ == "__main__":
    from lexer import tokenize
    
    test_code = '''
    let x = 10
    let y = 20
    
    func add(a, b) {
        return a + b
    }
    
    if x > 5 {
        print(add(x, y))
    } else {
        print("x is small")
    }
    
    let i = 0
    while i < 5 {
        print(i)
        i = i + 1
    }
    '''
    
    try:
        tokens = tokenize(test_code)
        program = parse(tokens)
        print(print_ast(program))
    except Exception as e:
        print(f"Error: {e}")
