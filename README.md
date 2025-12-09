# MiniLang

MiniLang은 Python으로 구현된 간단한 프로그래밍 언어 인터프리터입니다.

## 목차

- [소개](#소개)
- [요구사항](#요구사항)
- [설치](#설치)
- [실행 방법](#실행-방법)
- [언어 기능](#언어-기능)
- [문법](#문법)
- [예제](#예제)
- [테스트](#테스트)

## 소개

MiniLang은 컴파일러/인터프리터 학습을 위해 설계된 교육용 프로그래밍 언어입니다. 
다음과 같은 핵심 기능을 포함합니다:

- 변수 선언 및 대입
- 산술, 비교, 논리 연산
- 조건문 (if/else)
- 반복문 (while/for)
- 함수 정의 및 호출
- 배열 지원
- 내장 함수

## 요구사항

- Python 3.8 이상
- 추가 의존성 없음 (표준 라이브러리만 사용)

## 설치

```bash
# 저장소 복제 또는 파일 다운로드
cd minilang

# 실행 권한 부여 (선택사항)
chmod +x src/main.py
```

## 실행 방법

### 대화형 REPL 모드

```bash
python src/main.py
```

또는

```bash
cd src
python main.py
```

### 파일 실행

```bash
python src/main.py examples/hello_world.ml
```

### 디버그 모드 (토큰, AST 출력)

```bash
python src/main.py -d examples/fibonacci.ml
```

### 직접 코드 실행

```bash
python src/main.py -c "print(1 + 2 * 3)"
```

### 토큰 확인

```bash
python src/main.py -t "let x = 10"
```

### AST 확인

```bash
python src/main.py -a "let x = 10"
```

## 언어 기능

### 1. 변수 선언 및 대입

```javascript
let x = 10
let name = "MiniLang"
let pi = 3.14159
let flag = true
let arr = [1, 2, 3]
```

### 2. 연산자

**산술 연산자:**
```javascript
+   // 덧셈
-   // 뺄셈
*   // 곱셈
/   // 나눗셈
%   // 나머지
**  // 거듭제곱
```

**비교 연산자:**
```javascript
==  // 동등
!=  // 부등
<   // 미만
>   // 초과
<=  // 이하
>=  // 이상
```

**논리 연산자:**
```javascript
and  // 논리 AND
or   // 논리 OR
not  // 논리 NOT
```

**복합 대입 연산자:**
```javascript
+=  -= *= /=
```

### 3. 조건문

```javascript
if condition {
    // then block
} else if condition2 {
    // else if block
} else {
    // else block
}
```

### 4. 반복문

**While 문:**
```javascript
while condition {
    // body
}
```

**For 문:**
```javascript
for let i = 0; i < 10; i = i + 1 {
    // body
}
```

**제어문:**
```javascript
break     // 반복문 탈출
continue  // 다음 반복으로 건너뛰기
```

### 5. 함수

```javascript
func add(a, b) {
    return a + b
}

let result = add(3, 5)
```

### 6. 배열

```javascript
let arr = [1, 2, 3, 4, 5]
print(arr[0])        // 인덱스 접근
push(arr, 6)         // 요소 추가
let last = pop(arr)  // 요소 제거
print(len(arr))      // 길이
```

### 7. 내장 함수

| 함수 | 설명 |
|------|------|
| `print(args...)` | 출력 |
| `input(prompt)` | 입력 |
| `len(x)` | 길이 |
| `type(x)` | 타입 |
| `str(x)` | 문자열 변환 |
| `int(x)` | 정수 변환 |
| `float(x)` | 실수 변환 |
| `abs(x)` | 절대값 |
| `min(args...)` | 최소값 |
| `max(args...)` | 최대값 |
| `sqrt(x)` | 제곱근 |
| `floor(x)` | 내림 |
| `ceil(x)` | 올림 |
| `push(arr, val)` | 배열에 추가 |
| `pop(arr)` | 배열에서 제거 |
| `range(...)` | 범위 배열 생성 |

### 8. 주석

```javascript
// 단일 행 주석
# 이것도 주석

/* 다중 행
   주석 */
```

## 문법 (EBNF)

```ebnf
program        = { declaration } ;

declaration    = varDecl | funcDecl | statement ;

varDecl        = "let" IDENTIFIER [ "=" expression ] terminator ;

funcDecl       = "func" IDENTIFIER "(" [ parameters ] ")" block ;

parameters     = IDENTIFIER { "," IDENTIFIER } ;

statement      = exprStmt
               | ifStmt
               | whileStmt
               | forStmt
               | returnStmt
               | breakStmt
               | continueStmt
               | printStmt
               | block ;

exprStmt       = expression terminator ;

ifStmt         = "if" expression block [ "else" ( ifStmt | block ) ] ;

whileStmt      = "while" expression block ;

forStmt        = "for" [ varDecl | exprStmt ] ";" [ expression ] ";" [ expression ] block ;

returnStmt     = "return" [ expression ] terminator ;

breakStmt      = "break" terminator ;

continueStmt   = "continue" terminator ;

printStmt      = "print" "(" [ arguments ] ")" terminator ;

block          = "{" { declaration } "}" ;

expression     = assignment ;

assignment     = IDENTIFIER ( "=" | "+=" | "-=" | "*=" | "/=" ) assignment
               | logicOr ;

logicOr        = logicAnd { "or" logicAnd } ;

logicAnd       = equality { "and" equality } ;

equality       = comparison { ( "==" | "!=" ) comparison } ;

comparison     = term { ( "<" | ">" | "<=" | ">=" ) term } ;

term           = factor { ( "+" | "-" ) factor } ;

factor         = power { ( "*" | "/" | "%" ) power } ;

power          = unary { "**" unary } ;

unary          = ( "-" | "not" | "!" ) unary | postfix ;

postfix        = primary { call | index } ;

call           = "(" [ arguments ] ")" ;

index          = "[" expression "]" ;

primary        = NUMBER | STRING | "true" | "false" | "null"
               | IDENTIFIER | "(" expression ")" | arrayLiteral ;

arrayLiteral   = "[" [ arguments ] "]" ;

arguments      = expression { "," expression } ;

terminator     = ";" | NEWLINE ;
```

## 예제

### Hello World

```javascript
print("Hello, World!")
```

### 피보나치 수열

```javascript
func fib(n) {
    if n <= 1 {
        return n
    }
    return fib(n - 1) + fib(n - 2)
}

for let i = 0; i < 10; i = i + 1 {
    print(fib(i))
}
```

### FizzBuzz

```javascript
for let i = 1; i <= 100; i = i + 1 {
    if i % 15 == 0 {
        print("FizzBuzz")
    } else if i % 3 == 0 {
        print("Fizz")
    } else if i % 5 == 0 {
        print("Buzz")
    } else {
        print(i)
    }
}
```

## 테스트

```bash
# 모든 테스트 실행
python src/main.py tests/test01_variables.ml
python src/main.py tests/test02_comparison.ml
python src/main.py tests/test03_conditionals.ml
# ... 등등

# 또는 run_tests.sh 스크립트 사용
./run_tests.sh
```

## 프로젝트 구조

```
minilang/
├── src/
│   ├── tokens.py       # 토큰 정의
│   ├── lexer.py        # 어휘 분석기
│   ├── ast_nodes.py    # AST 노드 정의
│   ├── parser.py       # 구문 분석기
│   ├── interpreter.py  # 인터프리터
│   └── main.py         # 메인 실행 파일
├── tests/              # 테스트 프로그램
├── examples/           # 예제 프로그램
└── README.md           # 이 파일
```

## 라이선스

이 프로젝트는 교육 목적으로 제작되었습니다.

## 저자

컴파일러 수업 프로젝트
