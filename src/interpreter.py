"""
MiniLang Interpreter (인터프리터)
AST를 순회하며 프로그램을 실행합니다.
"""

from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from ast_nodes import *


class RuntimeError(Exception):
    """런타임 에러"""
    def __init__(self, message: str, line: int = 0, column: int = 0):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Runtime Error at line {line}: {message}")


class ReturnValue(Exception):
    """함수 반환을 위한 예외"""
    def __init__(self, value: Any):
        self.value = value


class BreakException(Exception):
    """break 문을 위한 예외"""
    pass


class ContinueException(Exception):
    """continue 문을 위한 예외"""
    pass


@dataclass
class Function:
    """사용자 정의 함수"""
    name: str
    parameters: List[str]
    body: Block
    closure: 'Environment'


@dataclass
class BuiltinFunction:
    """내장 함수"""
    name: str
    func: Callable
    arity: int  # 인자 개수 (-1은 가변)


class Environment:
    """변수 환경 (스코프)"""
    
    def __init__(self, parent: Optional['Environment'] = None):
        self.variables: Dict[str, Any] = {}
        self.parent = parent
    
    def define(self, name: str, value: Any):
        """변수 정의"""
        self.variables[name] = value
    
    def get(self, name: str) -> Any:
        """변수 값 조회"""
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.get(name)
        raise RuntimeError(f"Undefined variable: '{name}'")
    
    def set(self, name: str, value: Any):
        """변수 값 설정"""
        if name in self.variables:
            self.variables[name] = value
            return
        if self.parent:
            self.parent.set(name, value)
            return
        raise RuntimeError(f"Undefined variable: '{name}'")
    
    def exists(self, name: str) -> bool:
        """변수 존재 여부"""
        if name in self.variables:
            return True
        if self.parent:
            return self.parent.exists(name)
        return False


class Interpreter(ASTVisitor):
    """인터프리터 클래스"""
    
    def __init__(self):
        self.global_env = Environment()
        self.current_env = self.global_env
        self.output: List[str] = []  # 출력 버퍼
        self._setup_builtins()
    
    def _setup_builtins(self):
        """내장 함수 설정"""
        # len 함수
        self.global_env.define('len', BuiltinFunction(
            name='len',
            func=lambda args: len(args[0]) if args else 0,
            arity=1
        ))
        
        # type 함수
        def type_func(args):
            if not args:
                return 'null'
            val = args[0]
            if val is None:
                return 'null'
            if isinstance(val, bool):
                return 'boolean'
            if isinstance(val, int):
                return 'integer'
            if isinstance(val, float):
                return 'float'
            if isinstance(val, str):
                return 'string'
            if isinstance(val, list):
                return 'array'
            if isinstance(val, (Function, BuiltinFunction)):
                return 'function'
            return 'unknown'
        
        self.global_env.define('type', BuiltinFunction(
            name='type',
            func=type_func,
            arity=1
        ))
        
        # str 함수
        self.global_env.define('str', BuiltinFunction(
            name='str',
            func=lambda args: self._to_string(args[0]) if args else '',
            arity=1
        ))
        
        # int 함수
        def int_func(args):
            if not args:
                return 0
            val = args[0]
            if isinstance(val, bool):
                return 1 if val else 0
            if isinstance(val, (int, float)):
                return int(val)
            if isinstance(val, str):
                try:
                    return int(float(val))
                except ValueError:
                    raise RuntimeError(f"Cannot convert '{val}' to integer")
            raise RuntimeError(f"Cannot convert to integer")
        
        self.global_env.define('int', BuiltinFunction(
            name='int',
            func=int_func,
            arity=1
        ))
        
        # float 함수
        def float_func(args):
            if not args:
                return 0.0
            val = args[0]
            if isinstance(val, bool):
                return 1.0 if val else 0.0
            if isinstance(val, (int, float)):
                return float(val)
            if isinstance(val, str):
                try:
                    return float(val)
                except ValueError:
                    raise RuntimeError(f"Cannot convert '{val}' to float")
            raise RuntimeError(f"Cannot convert to float")
        
        self.global_env.define('float', BuiltinFunction(
            name='float',
            func=float_func,
            arity=1
        ))
        
        # abs 함수
        self.global_env.define('abs', BuiltinFunction(
            name='abs',
            func=lambda args: abs(args[0]) if args else 0,
            arity=1
        ))
        
        # min/max 함수
        self.global_env.define('min', BuiltinFunction(
            name='min',
            func=lambda args: min(args) if args else None,
            arity=-1
        ))
        
        self.global_env.define('max', BuiltinFunction(
            name='max',
            func=lambda args: max(args) if args else None,
            arity=-1
        ))
        
        # push 함수 (배열에 요소 추가)
        def push_func(args):
            if len(args) < 2:
                raise RuntimeError("push requires array and value")
            arr, val = args[0], args[1]
            if not isinstance(arr, list):
                raise RuntimeError("First argument must be an array")
            arr.append(val)
            return arr
        
        self.global_env.define('push', BuiltinFunction(
            name='push',
            func=push_func,
            arity=2
        ))
        
        # pop 함수
        def pop_func(args):
            if not args:
                raise RuntimeError("pop requires an array")
            arr = args[0]
            if not isinstance(arr, list):
                raise RuntimeError("Argument must be an array")
            if not arr:
                raise RuntimeError("Cannot pop from empty array")
            return arr.pop()
        
        self.global_env.define('pop', BuiltinFunction(
            name='pop',
            func=pop_func,
            arity=1
        ))
        
        # range 함수
        def range_func(args):
            if len(args) == 1:
                return list(range(int(args[0])))
            elif len(args) == 2:
                return list(range(int(args[0]), int(args[1])))
            elif len(args) >= 3:
                return list(range(int(args[0]), int(args[1]), int(args[2])))
            return []
        
        self.global_env.define('range', BuiltinFunction(
            name='range',
            func=range_func,
            arity=-1
        ))
        
        # sqrt 함수
        import math
        self.global_env.define('sqrt', BuiltinFunction(
            name='sqrt',
            func=lambda args: math.sqrt(args[0]) if args else 0,
            arity=1
        ))
        
        # floor/ceil 함수
        self.global_env.define('floor', BuiltinFunction(
            name='floor',
            func=lambda args: math.floor(args[0]) if args else 0,
            arity=1
        ))
        
        self.global_env.define('ceil', BuiltinFunction(
            name='ceil',
            func=lambda args: math.ceil(args[0]) if args else 0,
            arity=1
        ))
    
    def _to_string(self, value: Any) -> str:
        """값을 문자열로 변환"""
        if value is None:
            return "null"
        if isinstance(value, bool):
            return "true" if value else "false"
        if isinstance(value, list):
            elements = ", ".join(self._to_string(e) for e in value)
            return f"[{elements}]"
        if isinstance(value, Function):
            return f"<function {value.name}>"
        if isinstance(value, BuiltinFunction):
            return f"<builtin {value.name}>"
        return str(value)
    
    def _is_truthy(self, value: Any) -> bool:
        """값의 참/거짓 판단"""
        if value is None:
            return False
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return value != 0
        if isinstance(value, str):
            return len(value) > 0
        if isinstance(value, list):
            return len(value) > 0
        return True
    
    def execute(self, program: Program) -> Any:
        """프로그램 실행"""
        result = None
        for stmt in program.statements:
            result = self.visit(stmt)
        return result
    
    def execute_block(self, block: Block, environment: Environment) -> Any:
        """블록 실행 (새 스코프에서)"""
        previous_env = self.current_env
        self.current_env = environment
        
        try:
            result = None
            for stmt in block.statements:
                result = self.visit(stmt)
            return result
        finally:
            self.current_env = previous_env
    
    # =====================================================
    # 문장 방문
    # =====================================================
    
    def visit_Program(self, node: Program) -> Any:
        return self.execute(node)
    
    def visit_ExpressionStatement(self, node: ExpressionStatement) -> Any:
        return self.visit(node.expression)
    
    def visit_VariableDeclaration(self, node: VariableDeclaration) -> None:
        value = None
        if node.initializer:
            value = self.visit(node.initializer)
        self.current_env.define(node.name, value)
    
    def visit_Block(self, node: Block) -> Any:
        new_env = Environment(parent=self.current_env)
        return self.execute_block(node, new_env)
    
    def visit_IfStatement(self, node: IfStatement) -> Any:
        condition = self.visit(node.condition)
        
        if self._is_truthy(condition):
            return self.visit(node.then_branch)
        elif node.else_branch:
            return self.visit(node.else_branch)
        
        return None
    
    def visit_WhileStatement(self, node: WhileStatement) -> Any:
        result = None
        while self._is_truthy(self.visit(node.condition)):
            try:
                result = self.visit(node.body)
            except BreakException:
                break
            except ContinueException:
                continue
        return result
    
    def visit_ForStatement(self, node: ForStatement) -> Any:
        # for문을 위한 새 스코프 생성
        new_env = Environment(parent=self.current_env)
        previous_env = self.current_env
        self.current_env = new_env
        
        try:
            # 초기화
            if node.initializer:
                self.visit(node.initializer)
            
            result = None
            while True:
                # 조건 확인
                if node.condition:
                    if not self._is_truthy(self.visit(node.condition)):
                        break
                
                # 본문 실행
                try:
                    result = self.visit(node.body)
                except BreakException:
                    break
                except ContinueException:
                    pass
                
                # 증감
                if node.increment:
                    self.visit(node.increment)
            
            return result
        finally:
            self.current_env = previous_env
    
    def visit_FunctionDeclaration(self, node: FunctionDeclaration) -> None:
        func = Function(
            name=node.name,
            parameters=node.parameters,
            body=node.body,
            closure=self.current_env
        )
        self.current_env.define(node.name, func)
    
    def visit_ReturnStatement(self, node: ReturnStatement) -> None:
        value = None
        if node.value:
            value = self.visit(node.value)
        raise ReturnValue(value)
    
    def visit_BreakStatement(self, node: BreakStatement) -> None:
        raise BreakException()
    
    def visit_ContinueStatement(self, node: ContinueStatement) -> None:
        raise ContinueException()
    
    def visit_PrintStatement(self, node: PrintStatement) -> None:
        values = [self._to_string(self.visit(arg)) for arg in node.arguments]
        output = " ".join(values)
        print(output)
        self.output.append(output)
    
    # =====================================================
    # 표현식 방문
    # =====================================================
    
    def visit_NumberLiteral(self, node: NumberLiteral) -> Any:
        return node.value
    
    def visit_StringLiteral(self, node: StringLiteral) -> str:
        return node.value
    
    def visit_BooleanLiteral(self, node: BooleanLiteral) -> bool:
        return node.value
    
    def visit_NullLiteral(self, node: NullLiteral) -> None:
        return None
    
    def visit_Identifier(self, node: Identifier) -> Any:
        return self.current_env.get(node.name)
    
    def visit_ArrayLiteral(self, node: ArrayLiteral) -> list:
        return [self.visit(elem) for elem in node.elements]
    
    def visit_ArrayAccess(self, node: ArrayAccess) -> Any:
        array = self.visit(node.array)
        index = self.visit(node.index)
        
        if isinstance(array, list):
            if not isinstance(index, int):
                raise RuntimeError(f"Array index must be an integer", node.line, node.column)
            if index < 0 or index >= len(array):
                raise RuntimeError(f"Array index out of bounds: {index}", node.line, node.column)
            return array[index]
        
        if isinstance(array, str):
            if not isinstance(index, int):
                raise RuntimeError(f"String index must be an integer", node.line, node.column)
            if index < 0 or index >= len(array):
                raise RuntimeError(f"String index out of bounds: {index}", node.line, node.column)
            return array[index]
        
        raise RuntimeError(f"Cannot index type: {type(array).__name__}", node.line, node.column)
    
    def visit_ArrayIndexAssignment(self, node: 'ArrayIndexAssignment') -> Any:
        """배열 인덱스 대입"""
        array = self.visit(node.array)
        index = self.visit(node.index)
        value = self.visit(node.value)
        
        if not isinstance(array, list):
            raise RuntimeError(f"Cannot assign to index of non-array type", node.line, node.column)
        if not isinstance(index, int):
            raise RuntimeError(f"Array index must be an integer", node.line, node.column)
        if index < 0 or index >= len(array):
            raise RuntimeError(f"Array index out of bounds: {index}", node.line, node.column)
        
        if node.operator == '=':
            array[index] = value
        elif node.operator == '+=':
            array[index] = array[index] + value
        elif node.operator == '-=':
            array[index] = array[index] - value
        elif node.operator == '*=':
            array[index] = array[index] * value
        elif node.operator == '/=':
            if value == 0:
                raise RuntimeError("Division by zero", node.line, node.column)
            array[index] = array[index] / value
        else:
            raise RuntimeError(f"Unknown assignment operator: {node.operator}", node.line, node.column)
        
        return array[index]
    
    def visit_BinaryOp(self, node: BinaryOp) -> Any:
        # 단락 평가 (short-circuit evaluation)
        if node.operator == 'and':
            left = self.visit(node.left)
            if not self._is_truthy(left):
                return left
            return self.visit(node.right)
        
        if node.operator == 'or':
            left = self.visit(node.left)
            if self._is_truthy(left):
                return left
            return self.visit(node.right)
        
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        # 산술 연산
        if node.operator == '+':
            if isinstance(left, str) or isinstance(right, str):
                return self._to_string(left) + self._to_string(right)
            if isinstance(left, list) and isinstance(right, list):
                return left + right
            return left + right
        
        if node.operator == '-':
            return left - right
        
        if node.operator == '*':
            if isinstance(left, str) and isinstance(right, int):
                return left * right
            if isinstance(left, int) and isinstance(right, str):
                return left * right
            if isinstance(left, list) and isinstance(right, int):
                return left * right
            return left * right
        
        if node.operator == '/':
            if right == 0:
                raise RuntimeError("Division by zero", node.line, node.column)
            return left / right
        
        if node.operator == '%':
            if right == 0:
                raise RuntimeError("Modulo by zero", node.line, node.column)
            return left % right
        
        if node.operator == '**':
            return left ** right
        
        # 비교 연산
        if node.operator == '==':
            return left == right
        
        if node.operator == '!=':
            return left != right
        
        if node.operator == '<':
            return left < right
        
        if node.operator == '>':
            return left > right
        
        if node.operator == '<=':
            return left <= right
        
        if node.operator == '>=':
            return left >= right
        
        raise RuntimeError(f"Unknown operator: {node.operator}", node.line, node.column)
    
    def visit_UnaryOp(self, node: UnaryOp) -> Any:
        operand = self.visit(node.operand)
        
        if node.operator == '-':
            return -operand
        
        if node.operator == 'not':
            return not self._is_truthy(operand)
        
        raise RuntimeError(f"Unknown unary operator: {node.operator}", node.line, node.column)
    
    def visit_Assignment(self, node: Assignment) -> Any:
        value = self.visit(node.value)
        
        if node.operator == '=':
            # 변수가 없으면 새로 정의
            if not self.current_env.exists(node.target.name):
                self.current_env.define(node.target.name, value)
            else:
                self.current_env.set(node.target.name, value)
            return value
        
        # 복합 대입 연산자
        current = self.current_env.get(node.target.name)
        
        if node.operator == '+=':
            if isinstance(current, str) or isinstance(value, str):
                new_value = self._to_string(current) + self._to_string(value)
            else:
                new_value = current + value
        elif node.operator == '-=':
            new_value = current - value
        elif node.operator == '*=':
            new_value = current * value
        elif node.operator == '/=':
            if value == 0:
                raise RuntimeError("Division by zero", node.line, node.column)
            new_value = current / value
        else:
            raise RuntimeError(f"Unknown assignment operator: {node.operator}", node.line, node.column)
        
        self.current_env.set(node.target.name, new_value)
        return new_value
    
    def visit_FunctionCall(self, node: FunctionCall) -> Any:
        # input 함수 특별 처리
        if node.name == 'input':
            prompt = ""
            if node.arguments:
                prompt = self._to_string(self.visit(node.arguments[0]))
            try:
                return input(prompt)
            except EOFError:
                return ""
        
        # 함수 조회
        callee = self.current_env.get(node.name)
        
        # 인자 평가
        arguments = [self.visit(arg) for arg in node.arguments]
        
        # 내장 함수
        if isinstance(callee, BuiltinFunction):
            if callee.arity != -1 and len(arguments) != callee.arity:
                raise RuntimeError(
                    f"Function '{callee.name}' expects {callee.arity} arguments, got {len(arguments)}",
                    node.line, node.column
                )
            return callee.func(arguments)
        
        # 사용자 정의 함수
        if isinstance(callee, Function):
            if len(arguments) != len(callee.parameters):
                raise RuntimeError(
                    f"Function '{callee.name}' expects {len(callee.parameters)} arguments, got {len(arguments)}",
                    node.line, node.column
                )
            
            # 새 환경 생성 (클로저 기반)
            func_env = Environment(parent=callee.closure)
            for param, arg in zip(callee.parameters, arguments):
                func_env.define(param, arg)
            
            # 함수 본문 실행
            try:
                self.execute_block(callee.body, func_env)
                return None
            except ReturnValue as ret:
                return ret.value
        
        raise RuntimeError(f"'{node.name}' is not a function", node.line, node.column)


def interpret(program: Program) -> Any:
    """편의 함수: 프로그램 실행"""
    interpreter = Interpreter()
    return interpreter.execute(program)


if __name__ == "__main__":
    from lexer import tokenize
    from parser import parse
    
    test_code = '''
    // 피보나치 테스트
    func fib(n) {
        if n <= 1 {
            return n
        }
        return fib(n - 1) + fib(n - 2)
    }
    
    print("Fibonacci numbers:")
    let i = 0
    while i < 10 {
        print(fib(i))
        i = i + 1
    }
    
    // 배열 테스트
    let arr = [1, 2, 3, 4, 5]
    print("Array:", arr)
    print("Length:", len(arr))
    print("First element:", arr[0])
    '''
    
    try:
        tokens = tokenize(test_code)
        program = parse(tokens)
        interpret(program)
    except Exception as e:
        print(f"Error: {e}")
