// Test 8: 내장 함수
// 목적: 모든 내장 함수 테스트
// 기대 결과: 내장 함수들이 올바르게 동작함

print("=== 내장 함수 테스트 ===")

// len - 길이
print("\n--- len() ---")
print("len([1,2,3]) =", len([1, 2, 3]))
print("len('hello') =", len("hello"))
print("len([]) =", len([]))

// type - 타입 확인
print("\n--- type() ---")
print("type(42) =", type(42))
print("type(3.14) =", type(3.14))
print("type('hello') =", type("hello"))
print("type(true) =", type(true))
print("type([1,2]) =", type([1, 2]))
print("type(null) =", type(null))

// str - 문자열 변환
print("\n--- str() ---")
print("str(123) =", str(123))
print("str(3.14) =", str(3.14))
print("str(true) =", str(true))
print("str([1,2,3]) =", str([1, 2, 3]))

// int - 정수 변환
print("\n--- int() ---")
print("int(3.7) =", int(3.7))
print("int('42') =", int("42"))
print("int(true) =", int(true))
print("int(false) =", int(false))

// float - 실수 변환
print("\n--- float() ---")
print("float(42) =", float(42))
print("float('3.14') =", float("3.14"))

// abs - 절대값
print("\n--- abs() ---")
print("abs(-10) =", abs(-10))
print("abs(10) =", abs(10))
print("abs(-3.14) =", abs(-3.14))

// min/max
print("\n--- min() / max() ---")
print("min(3, 1, 4, 1, 5) =", min(3, 1, 4, 1, 5))
print("max(3, 1, 4, 1, 5) =", max(3, 1, 4, 1, 5))
print("min(10, 20) =", min(10, 20))
print("max(10, 20) =", max(10, 20))

// sqrt - 제곱근
print("\n--- sqrt() ---")
print("sqrt(16) =", sqrt(16))
print("sqrt(2) =", sqrt(2))
print("sqrt(100) =", sqrt(100))

// floor/ceil - 내림/올림
print("\n--- floor() / ceil() ---")
print("floor(3.7) =", floor(3.7))
print("floor(3.2) =", floor(3.2))
print("ceil(3.2) =", ceil(3.2))
print("ceil(3.7) =", ceil(3.7))
print("floor(-3.7) =", floor(-3.7))
print("ceil(-3.7) =", ceil(-3.7))

// push/pop - 배열 조작
print("\n--- push() / pop() ---")
let arr = [1, 2, 3]
print("원본:", arr)
push(arr, 4)
print("push(arr, 4):", arr)
let last = pop(arr)
print("pop(arr) 반환:", last)
print("pop 후:", arr)

// range - 범위 생성
print("\n--- range() ---")
print("range(5) =", range(5))
print("range(1, 6) =", range(1, 6))
print("range(0, 10, 2) =", range(0, 10, 2))
print("range(10, 0, -2) =", range(10, 0, -2))

// 복합 사용
print("\n--- 복합 사용 ---")

// 배열 합계 헬퍼 함수 (먼저 정의)
func arraySum(arr) {
    let sum = 0
    let i = 0
    while i < len(arr) {
        sum = sum + arr[i]
        i = i + 1
    }
    return sum
}

let numbers = range(1, 11)
print("numbers:", numbers)
print("합계:", arraySum(numbers))
print("최소:", min(3, 7, 1, 9, 2))
print("최대:", max(3, 7, 1, 9, 2))

print("\n=== 테스트 8 완료 ===")
