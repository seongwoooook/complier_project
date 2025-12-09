// Test 11: 복합 알고리즘
// 목적: 다양한 알고리즘 구현으로 언어 기능 종합 테스트
// 기대 결과: 알고리즘이 올바른 결과를 출력

print("=== 알고리즘 테스트 ===")

// 1. 버블 정렬
print("\n--- 버블 정렬 ---")
func bubbleSort(arr) {
    let n = len(arr)
    for let i = 0; i < n - 1; i = i + 1 {
        for let j = 0; j < n - i - 1; j = j + 1 {
            if arr[j] > arr[j + 1] {
                // 교환
                let temp = arr[j]
                arr[j] = arr[j + 1]
                arr[j + 1] = temp
            }
        }
    }
    return arr
}

let unsorted = [64, 34, 25, 12, 22, 11, 90]
print("정렬 전:", unsorted)
bubbleSort(unsorted)
print("정렬 후:", unsorted)

// 2. 이진 탐색
print("\n--- 이진 탐색 ---")
func binarySearch(arr, target) {
    let left = 0
    let right = len(arr) - 1
    
    while left <= right {
        let mid = floor((left + right) / 2)
        if arr[mid] == target {
            return mid
        } else if arr[mid] < target {
            left = mid + 1
        } else {
            right = mid - 1
        }
    }
    return -1
}

let sorted = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
print("배열:", sorted)
print("7의 위치:", binarySearch(sorted, 7))
print("11의 위치:", binarySearch(sorted, 11))
print("4의 위치:", binarySearch(sorted, 4))

// 3. 최대공약수 (유클리드 호제법)
print("\n--- 최대공약수 (GCD) ---")
func gcd(a, b) {
    while b != 0 {
        let temp = b
        b = a % b
        a = temp
    }
    return a
}

print("gcd(48, 18) =", gcd(48, 18))
print("gcd(100, 25) =", gcd(100, 25))
print("gcd(17, 13) =", gcd(17, 13))

// 4. 최소공배수
print("\n--- 최소공배수 (LCM) ---")
func lcm(a, b) {
    return (a * b) / gcd(a, b)
}

print("lcm(4, 6) =", lcm(4, 6))
print("lcm(21, 6) =", lcm(21, 6))

// 5. 소수 판별
print("\n--- 소수 판별 ---")
func isPrime(n) {
    if n < 2 {
        return false
    }
    if n == 2 {
        return true
    }
    if n % 2 == 0 {
        return false
    }
    let i = 3
    while i * i <= n {
        if n % i == 0 {
            return false
        }
        i = i + 2
    }
    return true
}

print("2-20 중 소수:")
for let n = 2; n <= 20; n = n + 1 {
    if isPrime(n) {
        print(n, "는 소수")
    }
}

// 6. 피보나치 (메모이제이션 없이)
print("\n--- 피보나치 (반복) ---")
func fibIterative(n) {
    if n <= 1 {
        return n
    }
    let prev = 0
    let curr = 1
    for let i = 2; i <= n; i = i + 1 {
        let next = prev + curr
        prev = curr
        curr = next
    }
    return curr
}

print("처음 15개 피보나치:")
for let i = 0; i < 15; i = i + 1 {
    print("F(" + str(i) + ") =", fibIterative(i))
}

// 7. 배열 뒤집기
print("\n--- 배열 뒤집기 ---")
func reverseArray(arr) {
    let result = []
    let i = len(arr) - 1
    while i >= 0 {
        push(result, arr[i])
        i = i - 1
    }
    return result
}

let original = [1, 2, 3, 4, 5]
print("원본:", original)
print("뒤집기:", reverseArray(original))

// 8. 배열에서 최대값/최소값 인덱스
print("\n--- 최대/최소 인덱스 ---")
func maxIndex(arr) {
    let maxIdx = 0
    for let i = 1; i < len(arr); i = i + 1 {
        if arr[i] > arr[maxIdx] {
            maxIdx = i
        }
    }
    return maxIdx
}

let values = [3, 7, 2, 9, 1, 5, 8]
print("배열:", values)
print("최대값 인덱스:", maxIndex(values))
print("최대값:", values[maxIndex(values)])

print("\n=== 테스트 11 완료 ===")
