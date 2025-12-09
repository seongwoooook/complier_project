// Test 7: 배열
// 목적: 배열 리터럴, 인덱스 접근, 배열 연산 테스트
// 기대 결과: 배열이 올바르게 생성되고 조작됨

print("=== 배열 테스트 ===")

// 배열 생성
let numbers = [1, 2, 3, 4, 5]
let fruits = ["apple", "banana", "cherry"]
let mixed = [1, "two", 3.14, true, null]

print("numbers:", numbers)
print("fruits:", fruits)
print("mixed:", mixed)

// 인덱스 접근
print("\n인덱스 접근:")
print("numbers[0] =", numbers[0])
print("numbers[2] =", numbers[2])
print("fruits[1] =", fruits[1])

// 배열 길이
print("\n배열 길이:")
print("len(numbers) =", len(numbers))
print("len(fruits) =", len(fruits))

// 배열 순회
print("\n배열 순회:")
let i = 0
while i < len(numbers) {
    print("numbers[" + str(i) + "] =", numbers[i])
    i = i + 1
}

// 배열 수정 (push)
print("\n배열 수정:")
let arr = [1, 2, 3]
print("원본:", arr)
push(arr, 4)
push(arr, 5)
print("push 후:", arr)

// pop
let popped = pop(arr)
print("pop 결과:", popped)
print("pop 후:", arr)

// 배열 합치기
print("\n배열 합치기:")
let a = [1, 2, 3]
let b = [4, 5, 6]
let c = a + b
print("[1,2,3] + [4,5,6] =", c)

// 빈 배열
let empty = []
print("\n빈 배열:", empty)
print("빈 배열 길이:", len(empty))

// 배열 요소 합계 함수
func arraySum(arr) {
    let sum = 0
    let i = 0
    while i < len(arr) {
        sum = sum + arr[i]
        i = i + 1
    }
    return sum
}

print("\narraySum([1,2,3,4,5]) =", arraySum(numbers))

// 최대값 찾기
func findMax(arr) {
    if len(arr) == 0 {
        return null
    }
    let maxVal = arr[0]
    let i = 1
    while i < len(arr) {
        if arr[i] > maxVal {
            maxVal = arr[i]
        }
        i = i + 1
    }
    return maxVal
}

let testArr = [3, 7, 2, 9, 1, 5]
print("findMax([3,7,2,9,1,5]) =", findMax(testArr))

// range 함수
print("\nrange 함수:")
print("range(5) =", range(5))
print("range(2, 8) =", range(2, 8))
print("range(0, 10, 2) =", range(0, 10, 2))

print("\n=== 테스트 7 완료 ===")
