// Test 6: 함수 정의 및 호출
// 목적: 사용자 정의 함수, 재귀 함수, 클로저 테스트
// 기대 결과: 함수가 올바르게 정의되고 호출됨

print("=== 함수 테스트 ===")

// 기본 함수
func greet(name) {
    print("Hello,", name, "!")
}

greet("World")
greet("MiniLang")

// 반환값이 있는 함수
func add(a, b) {
    return a + b
}

func multiply(a, b) {
    return a * b
}

print("\nadd(3, 5) =", add(3, 5))
print("multiply(4, 7) =", multiply(4, 7))

// 함수 조합
print("add(multiply(2, 3), 4) =", add(multiply(2, 3), 4))  // 10

// 조건이 있는 함수
func absoluteValue(n) {
    if n < 0 {
        return -n
    }
    return n
}

print("\nabsoluteValue(-5) =", absoluteValue(-5))
print("absoluteValue(10) =", absoluteValue(10))

// 재귀 함수: 팩토리얼
func factorial(n) {
    if n <= 1 {
        return 1
    }
    return n * factorial(n - 1)
}

print("\nfactorial(5) =", factorial(5))   // 120
print("factorial(10) =", factorial(10))   // 3628800

// 재귀 함수: 피보나치
func fib(n) {
    if n <= 1 {
        return n
    }
    return fib(n - 1) + fib(n - 2)
}

print("\n피보나치 수열 (처음 10개):")
for let i = 0; i < 10; i = i + 1 {
    print("fib(" + str(i) + ") =", fib(i))
}

// 여러 조건 분기 함수
func grade(score) {
    if score >= 90 {
        return "A"
    } else if score >= 80 {
        return "B"
    } else if score >= 70 {
        return "C"
    } else if score >= 60 {
        return "D"
    }
    return "F"
}

print("\ngrade(95) =", grade(95))
print("grade(83) =", grade(83))
print("grade(55) =", grade(55))

// 함수 내 지역 변수
func localTest() {
    let local = "지역 변수"
    print("함수 내부:", local)
    return local
}

let result = localTest()
print("반환값:", result)

print("\n=== 테스트 6 완료 ===")
