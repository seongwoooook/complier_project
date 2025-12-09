"""
MiniLang AST (Abstract Syntax Tree) Nodes
추상 구문 트리 노드 클래스들을 정의합니다.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any, Union
from abc import ABC, abstractmethod


class ASTNode(ABC):
    """AST 노드 기본 클래스"""
    line: int = 0
    column: int = 0


# ============================================
# 표현식 (Expressions)
# ============================================

@dataclass
class Expression(ASTNode):
    """표현식 기본 클래스"""
    pass


@dataclass
class NumberLiteral(Expression):
    """숫자 리터럴 (정수 또는 실수)"""
    value: Union[int, float]
    line: int = 0
    column: int = 0


@dataclass
class StringLiteral(Expression):
    """문자열 리터럴"""
    value: str
    line: int = 0
    column: int = 0


@dataclass
class BooleanLiteral(Expression):
    """불리언 리터럴"""
    value: bool
    line: int = 0
    column: int = 0


@dataclass
class NullLiteral(Expression):
    """Null 리터럴"""
    line: int = 0
    column: int = 0


@dataclass
class Identifier(Expression):
    """식별자 (변수명)"""
    name: str
    line: int = 0
    column: int = 0


@dataclass
class BinaryOp(Expression):
    """이항 연산"""
    left: Expression
    operator: str
    right: Expression
    line: int = 0
    column: int = 0


@dataclass
class UnaryOp(Expression):
    """단항 연산"""
    operator: str
    operand: Expression
    line: int = 0
    column: int = 0


@dataclass
class Assignment(Expression):
    """대입 표현식"""
    target: Identifier
    operator: str  # =, +=, -=, *=, /=
    value: Expression
    line: int = 0
    column: int = 0


@dataclass
class FunctionCall(Expression):
    """함수 호출"""
    name: str
    arguments: List[Expression]
    line: int = 0
    column: int = 0


@dataclass
class ArrayLiteral(Expression):
    """배열 리터럴"""
    elements: List[Expression]
    line: int = 0
    column: int = 0


@dataclass
class ArrayAccess(Expression):
    """배열 인덱스 접근"""
    array: Expression
    index: Expression
    line: int = 0
    column: int = 0


@dataclass
class ArrayIndexAssignment(Expression):
    """배열 인덱스 대입"""
    array: Expression
    index: Expression
    operator: str  # =, +=, -=, *=, /=
    value: Expression
    line: int = 0
    column: int = 0


@dataclass
class TernaryOp(Expression):
    """삼항 연산자 (condition ? then_expr : else_expr)"""
    condition: Expression
    then_expr: Expression
    else_expr: Expression
    line: int = 0
    column: int = 0


# ============================================
# 문장 (Statements)
# ============================================

@dataclass
class Statement(ASTNode):
    """문장 기본 클래스"""
    pass


@dataclass
class ExpressionStatement(Statement):
    """표현식 문장"""
    expression: Expression
    line: int = 0
    column: int = 0


@dataclass
class VariableDeclaration(Statement):
    """변수 선언"""
    name: str
    initializer: Optional[Expression]
    line: int = 0
    column: int = 0


@dataclass
class Block(Statement):
    """블록 (문장들의 집합)"""
    statements: List[Statement]
    line: int = 0
    column: int = 0


@dataclass
class IfStatement(Statement):
    """조건문"""
    condition: Expression
    then_branch: Statement
    else_branch: Optional[Statement]
    line: int = 0
    column: int = 0


@dataclass
class WhileStatement(Statement):
    """While 반복문"""
    condition: Expression
    body: Statement
    line: int = 0
    column: int = 0


@dataclass
class ForStatement(Statement):
    """For 반복문"""
    initializer: Optional[Statement]
    condition: Optional[Expression]
    increment: Optional[Expression]
    body: Statement
    line: int = 0
    column: int = 0


@dataclass
class FunctionDeclaration(Statement):
    """함수 선언"""
    name: str
    parameters: List[str]
    body: Block
    line: int = 0
    column: int = 0


@dataclass
class ReturnStatement(Statement):
    """Return 문"""
    value: Optional[Expression]
    line: int = 0
    column: int = 0


@dataclass
class BreakStatement(Statement):
    """Break 문"""
    line: int = 0
    column: int = 0


@dataclass
class ContinueStatement(Statement):
    """Continue 문"""
    line: int = 0
    column: int = 0


@dataclass
class PrintStatement(Statement):
    """Print 문 (내장 출력)"""
    arguments: List[Expression]
    line: int = 0
    column: int = 0


# ============================================
# 프로그램
# ============================================

@dataclass
class Program(ASTNode):
    """프로그램 (최상위 노드)"""
    statements: List[Statement]
    line: int = 0
    column: int = 0


# ============================================
# AST 방문자 패턴
# ============================================

class ASTVisitor(ABC):
    """AST 방문자 기본 클래스"""
    
    def visit(self, node: ASTNode) -> Any:
        """노드 방문"""
        method_name = f'visit_{node.__class__.__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node: ASTNode) -> Any:
        """기본 방문 메서드"""
        raise NotImplementedError(f"No visit method for {node.__class__.__name__}")


class ASTPrinter(ASTVisitor):
    """AST를 문자열로 출력하는 방문자"""
    
    def __init__(self):
        self.indent_level = 0
    
    def indent(self) -> str:
        return "  " * self.indent_level
    
    def visit_Program(self, node: Program) -> str:
        result = "Program:\n"
        self.indent_level += 1
        for stmt in node.statements:
            result += self.indent() + self.visit(stmt) + "\n"
        self.indent_level -= 1
        return result
    
    def visit_NumberLiteral(self, node: NumberLiteral) -> str:
        return f"Number({node.value})"
    
    def visit_StringLiteral(self, node: StringLiteral) -> str:
        return f'String("{node.value}")'
    
    def visit_BooleanLiteral(self, node: BooleanLiteral) -> str:
        return f"Boolean({node.value})"
    
    def visit_NullLiteral(self, node: NullLiteral) -> str:
        return "Null"
    
    def visit_Identifier(self, node: Identifier) -> str:
        return f"Identifier({node.name})"
    
    def visit_BinaryOp(self, node: BinaryOp) -> str:
        return f"BinaryOp({self.visit(node.left)} {node.operator} {self.visit(node.right)})"
    
    def visit_UnaryOp(self, node: UnaryOp) -> str:
        return f"UnaryOp({node.operator} {self.visit(node.operand)})"
    
    def visit_Assignment(self, node: Assignment) -> str:
        return f"Assignment({node.target.name} {node.operator} {self.visit(node.value)})"
    
    def visit_FunctionCall(self, node: FunctionCall) -> str:
        args = ", ".join(self.visit(arg) for arg in node.arguments)
        return f"FunctionCall({node.name}({args}))"
    
    def visit_ArrayLiteral(self, node: ArrayLiteral) -> str:
        elements = ", ".join(self.visit(elem) for elem in node.elements)
        return f"Array([{elements}])"
    
    def visit_ArrayAccess(self, node: ArrayAccess) -> str:
        return f"ArrayAccess({self.visit(node.array)}[{self.visit(node.index)}])"
    
    def visit_ArrayIndexAssignment(self, node: 'ArrayIndexAssignment') -> str:
        return f"ArrayIndexAssign({self.visit(node.array)}[{self.visit(node.index)}] {node.operator} {self.visit(node.value)})"
    
    def visit_ExpressionStatement(self, node: ExpressionStatement) -> str:
        return f"ExpressionStmt({self.visit(node.expression)})"
    
    def visit_VariableDeclaration(self, node: VariableDeclaration) -> str:
        if node.initializer:
            return f"VarDecl(let {node.name} = {self.visit(node.initializer)})"
        return f"VarDecl(let {node.name})"
    
    def visit_Block(self, node: Block) -> str:
        result = "Block:\n"
        self.indent_level += 1
        for stmt in node.statements:
            result += self.indent() + self.visit(stmt) + "\n"
        self.indent_level -= 1
        return result.rstrip()
    
    def visit_IfStatement(self, node: IfStatement) -> str:
        result = f"If({self.visit(node.condition)}):\n"
        self.indent_level += 1
        result += self.indent() + "Then: " + self.visit(node.then_branch) + "\n"
        if node.else_branch:
            result += self.indent() + "Else: " + self.visit(node.else_branch) + "\n"
        self.indent_level -= 1
        return result.rstrip()
    
    def visit_WhileStatement(self, node: WhileStatement) -> str:
        result = f"While({self.visit(node.condition)}):\n"
        self.indent_level += 1
        result += self.indent() + self.visit(node.body)
        self.indent_level -= 1
        return result
    
    def visit_ForStatement(self, node: ForStatement) -> str:
        init = self.visit(node.initializer) if node.initializer else "None"
        cond = self.visit(node.condition) if node.condition else "None"
        inc = self.visit(node.increment) if node.increment else "None"
        result = f"For({init}; {cond}; {inc}):\n"
        self.indent_level += 1
        result += self.indent() + self.visit(node.body)
        self.indent_level -= 1
        return result
    
    def visit_FunctionDeclaration(self, node: FunctionDeclaration) -> str:
        params = ", ".join(node.parameters)
        result = f"FuncDecl({node.name}({params})):\n"
        self.indent_level += 1
        result += self.indent() + self.visit(node.body)
        self.indent_level -= 1
        return result
    
    def visit_ReturnStatement(self, node: ReturnStatement) -> str:
        if node.value:
            return f"Return({self.visit(node.value)})"
        return "Return"
    
    def visit_BreakStatement(self, node: BreakStatement) -> str:
        return "Break"
    
    def visit_ContinueStatement(self, node: ContinueStatement) -> str:
        return "Continue"
    
    def visit_PrintStatement(self, node: PrintStatement) -> str:
        args = ", ".join(self.visit(arg) for arg in node.arguments)
        return f"Print({args})"


def print_ast(node: ASTNode) -> str:
    """AST를 문자열로 출력"""
    printer = ASTPrinter()
    return printer.visit(node)
