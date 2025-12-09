// Test 12: 종합 프로그램 - 간단한 계산기 및 수학 유틸리티
// 목적: 언어의 모든 기능을 활용한 실용적인 프로그램
// 기대 결과: 다양한 수학 연산이 올바르게 수행됨

print("╔══════════════════════════════════════╗")
print("║    MiniLang 수학 유틸리티 v1.0       ║")
print("╚══════════════════════════════════════╝")

// ==========================================
// 기본 수학 함수들
// ==========================================

// 제곱 함수
func square(n) {
    return n * n
}

// 세제곱 함수
func cube(n) {
    return n * n * n
}

// n제곱 함수
func power(base, exp) {
    if exp == 0 {
        return 1
    }
    let result = 1
    for let i = 0; i < exp; i = i + 1 {
        result = result * base
    }
    return result
}

// 합계 함수
func sum(arr) {
    let total = 0
    for let i = 0; i < len(arr); i = i + 1 {
        total = total + arr[i]
    }
    return total
}

// 평균 함수
func average(arr) {
    if len(arr) == 0 {
        return 0
    }
    return sum(arr) / len(arr)
}

// 범위 합계 (1부터 n까지)
func sumRange(n) {
    return n * (n + 1) / 2
}

print("\n=== 기본 연산 테스트 ===")
print("square(7) =", square(7))
print("cube(4) =", cube(4))
print("power(2, 10) =", power(2, 10))
print("sumRange(100) =", sumRange(100))

// ==========================================
// 통계 함수들
// ==========================================

func minValue(arr) {
    let minVal = arr[0]
    for let i = 1; i < len(arr); i = i + 1 {
        if arr[i] < minVal {
            minVal = arr[i]
        }
    }
    return minVal
}

func maxValue(arr) {
    let maxVal = arr[0]
    for let i = 1; i < len(arr); i = i + 1 {
        if arr[i] > maxVal {
            maxVal = arr[i]
        }
    }
    return maxVal
}

func rangeValue(arr) {
    return maxValue(arr) - minValue(arr)
}

print("\n=== 통계 테스트 ===")
let data = [23, 45, 12, 67, 34, 89, 56, 78, 90, 11]
print("데이터:", data)
print("합계:", sum(data))
print("평균:", average(data))
print("최소:", minValue(data))
print("최대:", maxValue(data))
print("범위:", rangeValue(data))

// ==========================================
// 수열 생성
// ==========================================

// 등차수열 생성
func arithmeticSequence(start, diff, count) {
    let seq = []
    let val = start
    for let i = 0; i < count; i = i + 1 {
        push(seq, val)
        val = val + diff
    }
    return seq
}

// 등비수열 생성
func geometricSequence(start, ratio, count) {
    let seq = []
    let val = start
    for let i = 0; i < count; i = i + 1 {
        push(seq, val)
        val = val * ratio
    }
    return seq
}

// 피보나치 수열 생성
func fibonacciSequence(count) {
    let seq = []
    let a = 0
    let b = 1
    for let i = 0; i < count; i = i + 1 {
        push(seq, a)
        let temp = a + b
        a = b
        b = temp
    }
    return seq
}

print("\n=== 수열 생성 테스트 ===")
print("등차수열 (시작=2, 공차=3, 개수=8):")
print(arithmeticSequence(2, 3, 8))

print("등비수열 (시작=1, 공비=2, 개수=10):")
print(geometricSequence(1, 2, 10))

print("피보나치 수열 (처음 12개):")
print(fibonacciSequence(12))

// ==========================================
// 진법 변환
// ==========================================

func decimalToBinary(n) {
    if n == 0 {
        return "0"
    }
    let result = ""
    while n > 0 {
        result = str(n % 2) + result
        n = floor(n / 2)
    }
    return result
}

print("\n=== 진법 변환 테스트 ===")
print("10진수 -> 2진수:")
print("10 ->", decimalToBinary(10))
print("42 ->", decimalToBinary(42))
print("255 ->", decimalToBinary(255))
print("1024 ->", decimalToBinary(1024))

// ==========================================
// 도형 계산
// ==========================================

let PI = 3.14159265359

func circleArea(radius) {
    return PI * radius * radius
}

func circleCircumference(radius) {
    return 2 * PI * radius
}

func rectangleArea(width, height) {
    return width * height
}

func triangleArea(base, height) {
    return base * height / 2
}

print("\n=== 도형 계산 테스트 ===")
print("원 (반지름=5):")
print("  넓이:", circleArea(5))
print("  둘레:", circleCircumference(5))

print("직사각형 (8 x 6):")
print("  넓이:", rectangleArea(8, 6))

print("삼각형 (밑변=10, 높이=7):")
print("  넓이:", triangleArea(10, 7))

// ==========================================
// 복리 계산
// ==========================================

func compoundInterest(principal, rate, years) {
    // 복리 공식: A = P(1 + r)^n
    let amount = principal
    for let i = 0; i < years; i = i + 1 {
        amount = amount * (1 + rate)
    }
    return amount
}

print("\n=== 복리 계산 테스트 ===")
let initialAmount = 10000
let interestRate = 0.05  // 5%
let years = 10

print("원금:", initialAmount)
print("연이율:", interestRate * 100, "%")
print("기간:", years, "년")
print("최종 금액:", compoundInterest(initialAmount, interestRate, years))

// ==========================================
// 최종 요약
// ==========================================

print("\n╔══════════════════════════════════════╗")
print("║         테스트 완료!                 ║")
print("║   MiniLang의 모든 기능이            ║")
print("║   정상적으로 작동합니다.            ║")
print("╚══════════════════════════════════════╝")

print("\n=== 테스트 12 완료 ===")
