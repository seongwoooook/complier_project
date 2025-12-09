#!/usr/bin/env python3
"""
MiniLang - A Simple Programming Language Interpreter
메인 실행 파일: REPL 및 파일 실행 지원
"""

import sys
import os
import argparse
from typing import Optional

# 소스 디렉토리를 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lexer import Lexer, LexerError, tokenize
from parser import Parser, ParseError, parse
from interpreter import Interpreter, RuntimeError as MiniLangRuntimeError, interpret
from ast_nodes import print_ast


VERSION = "1.0.0"

BANNER = f"""
╔══════════════════════════════════════════════════════════════╗
║                      MiniLang v{VERSION}                         ║
║           A Simple Programming Language Interpreter          ║
╚══════════════════════════════════════════════════════════════╝
Type 'help' for commands, 'exit' or Ctrl+D to quit.
"""


def print_help():
    """도움말 출력"""
    help_text = """
Available commands:
  help          - Show this help message
  exit, quit    - Exit the interpreter
  clear         - Clear the screen
  tokens <code> - Show tokens for the given code
  ast <code>    - Show AST for the given code
  run <file>    - Run a MiniLang file
  
Example usage:
  >>> let x = 10
  >>> print(x * 2)
  20
  >>> func greet(name) { print("Hello, " + name) }
  >>> greet("World")
  Hello, World
"""
    print(help_text)


def show_tokens(code: str):
    """토큰 출력"""
    try:
        tokens = tokenize(code)
        print("\nTokens:")
        for token in tokens:
            print(f"  {token}")
        print()
    except LexerError as e:
        print(f"Lexer Error: {e}")


def show_ast(code: str):
    """AST 출력"""
    try:
        tokens = tokenize(code)
        program = parse(tokens)
        print("\nAST:")
        print(print_ast(program))
    except LexerError as e:
        print(f"Lexer Error: {e}")
    except ParseError as e:
        print(f"Parse Error: {e}")


def run_file(filepath: str, show_debug: bool = False) -> bool:
    """파일 실행"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        
        if show_debug:
            print(f"\n=== Running: {filepath} ===\n")
        
        # 토큰화
        tokens = tokenize(code)
        
        if show_debug:
            print("Tokens:")
            for token in tokens[:20]:  # 처음 20개만
                print(f"  {token}")
            if len(tokens) > 20:
                print(f"  ... and {len(tokens) - 20} more tokens")
            print()
        
        # 파싱
        parser = Parser(tokens)
        program = parser.parse()
        
        if parser.errors:
            print("Parse Errors:")
            for error in parser.errors:
                print(f"  {error}")
            return False
        
        if show_debug:
            print("AST:")
            print(print_ast(program))
            print("\n=== Output ===\n")
        
        # 실행
        interpreter = Interpreter()
        interpreter.execute(program)
        
        return True
        
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        return False
    except LexerError as e:
        print(f"Lexer Error: {e}")
        return False
    except ParseError as e:
        print(f"Parse Error: {e}")
        return False
    except MiniLangRuntimeError as e:
        print(f"Runtime Error: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def repl():
    """대화형 REPL (Read-Eval-Print Loop)"""
    print(BANNER)
    
    interpreter = Interpreter()
    multiline_buffer = []
    brace_count = 0
    
    while True:
        try:
            # 프롬프트 결정
            if multiline_buffer:
                prompt = "... "
            else:
                prompt = ">>> "
            
            # 입력 받기
            line = input(prompt)
            
            # 특수 명령어 처리 (단일 행 모드에서만)
            if not multiline_buffer:
                stripped = line.strip()
                
                if stripped in ('exit', 'quit'):
                    print("Goodbye!")
                    break
                
                if stripped == 'help':
                    print_help()
                    continue
                
                if stripped == 'clear':
                    os.system('clear' if os.name == 'posix' else 'cls')
                    continue
                
                if stripped.startswith('tokens '):
                    show_tokens(stripped[7:])
                    continue
                
                if stripped.startswith('ast '):
                    show_ast(stripped[4:])
                    continue
                
                if stripped.startswith('run '):
                    run_file(stripped[4:].strip())
                    continue
            
            # 멀티라인 처리
            multiline_buffer.append(line)
            brace_count += line.count('{') - line.count('}')
            
            # 블록이 완성되지 않았으면 계속 입력 받기
            if brace_count > 0:
                continue
            
            # 코드 실행
            code = '\n'.join(multiline_buffer)
            multiline_buffer = []
            brace_count = 0
            
            if not code.strip():
                continue
            
            try:
                # 토큰화 및 파싱
                tokens = tokenize(code)
                parser = Parser(tokens)
                program = parser.parse()
                
                if parser.errors:
                    for error in parser.errors:
                        print(f"Parse Error: {error}")
                    continue
                
                # 실행
                result = interpreter.execute(program)
                
                # 표현식 결과 자동 출력 (REPL 편의 기능)
                if result is not None:
                    print(result)
                
            except LexerError as e:
                print(f"Lexer Error: {e}")
            except ParseError as e:
                print(f"Parse Error: {e}")
            except MiniLangRuntimeError as e:
                print(f"Runtime Error: {e}")
        
        except EOFError:
            print("\nGoodbye!")
            break
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")
            multiline_buffer = []
            brace_count = 0


def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(
        description='MiniLang Interpreter - A Simple Programming Language',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  minilang                    Start interactive REPL
  minilang script.ml          Run a MiniLang file
  minilang -d script.ml       Run with debug output
  minilang -t "let x = 10"    Show tokens
  minilang -a "let x = 10"    Show AST
"""
    )
    
    parser.add_argument('file', nargs='?', help='MiniLang source file to run')
    parser.add_argument('-v', '--version', action='version', version=f'MiniLang {VERSION}')
    parser.add_argument('-d', '--debug', action='store_true', help='Show debug information')
    parser.add_argument('-t', '--tokens', metavar='CODE', help='Show tokens for code')
    parser.add_argument('-a', '--ast', metavar='CODE', help='Show AST for code')
    parser.add_argument('-c', '--code', metavar='CODE', help='Execute code directly')
    
    args = parser.parse_args()
    
    # 토큰 출력
    if args.tokens:
        show_tokens(args.tokens)
        return
    
    # AST 출력
    if args.ast:
        show_ast(args.ast)
        return
    
    # 직접 코드 실행
    if args.code:
        try:
            tokens = tokenize(args.code)
            program = parse(tokens)
            interpret(program)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
        return
    
    # 파일 실행
    if args.file:
        success = run_file(args.file, show_debug=args.debug)
        sys.exit(0 if success else 1)
    
    # REPL 시작
    repl()


if __name__ == "__main__":
    main()
