// Example: 피보나치 수열 계산기
// 재귀와 반복 두 가지 방법으로 피보나치 수를 계산합니다.

print("=== 피보나치 수열 계산기 ===")

// 재귀 방식 (작은 n에 적합)
func fibRecursive(n) {
    if n <= 1 {
        return n
    }
    return fibRecursive(n - 1) + fibRecursive(n - 2)
}

// 반복 방식 (큰 n에 적합)
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

// 피보나치 수열 출력
print("\n처음 20개의 피보나치 수:")
for let i = 0; i < 20; i = i + 1 {
    print("F(" + str(i) + ") =", fibIterative(i))
}

// 피보나치 수열의 비율 (황금비에 수렴)
print("\n피보나치 비율 (황금비 수렴):")
for let i = 2; i < 15; i = i + 1 {
    let ratio = fibIterative(i) / fibIterative(i - 1)
    print("F(" + str(i) + ")/F(" + str(i-1) + ") =", ratio)
}

print("\n황금비 ≈ 1.618033988749...")
