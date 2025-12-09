// Test 2: 비교 및 논리 연산
// 목적: 비교 연산자와 논리 연산자 테스트
// 기대 결과: 모든 비교/논리 연산이 올바르게 동작

let x = 10
let y = 20
let z = 10

print("=== 비교 연산 테스트 ===")
print("x =", x, ", y =", y, ", z =", z)

// 비교 연산자
print("x == z:", x == z)      // true
print("x == y:", x == y)      // false
print("x != y:", x != y)      // true
print("x < y:", x < y)        // true
print("x > y:", x > y)        // false
print("x <= z:", x <= z)      // true
print("y >= x:", y >= x)      // true

print("\n=== 논리 연산 테스트 ===")

let a = true
let b = false

print("a =", a, ", b =", b)
print("a and b:", a and b)    // false
print("a or b:", a or b)      // true
print("not a:", not a)        // false
print("not b:", not b)        // true

// 복합 논리 연산
print("\n복합 논리 연산:")
print("(x < y) and (x == z):", (x < y) and (x == z))  // true
print("(x > y) or (x == z):", (x > y) or (x == z))    // true

// 단락 평가 (short-circuit)
print("\n단락 평가 테스트:")
print("false and (1/0):", false and (1 == 0))  // false (두 번째 평가 안 함)
print("true or (1/0):", true or (1 == 0))      // true (두 번째 평가 안 함)

print("\n=== 테스트 2 완료 ===")
