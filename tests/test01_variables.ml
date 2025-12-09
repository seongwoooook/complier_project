// Test 1: 변수 선언 및 기본 연산
// 목적: let 키워드를 사용한 변수 선언과 기본 산술 연산 테스트
// 기대 결과: 각 연산 결과가 올바르게 출력됨

// 변수 선언
let a = 10
let b = 20
let c = 3.14

// 산술 연산
print("=== 산술 연산 테스트 ===")
print("a =", a)
print("b =", b)
print("c =", c)

print("a + b =", a + b)       // 30
print("a - b =", a - b)       // -10
print("a * b =", a * b)       // 200
print("b / a =", b / a)       // 2.0
print("b % a =", b % a)       // 0
print("a ** 2 =", a ** 2)     // 100

// 복합 연산
let result = (a + b) * c / 2
print("(a + b) * c / 2 =", result)  // 47.1

// 문자열 연산
let name = "MiniLang"
let greeting = "Hello, " + name + "!"
print(greeting)  // Hello, MiniLang!

print("\n=== 테스트 1 완료 ===")
