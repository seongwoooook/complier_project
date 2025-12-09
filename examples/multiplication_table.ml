// Example: 구구단
// 중첩 반복문을 사용한 구구단 출력

print("=== 구구단 ===\n")

// 2단부터 9단까지 출력
for let i = 2; i <= 9; i = i + 1 {
    print("--- " + str(i) + "단 ---")
    for let j = 1; j <= 9; j = j + 1 {
        let result = i * j
        print(str(i) + " x " + str(j) + " = " + str(result))
    }
    print("")
}

// 특정 단 출력 함수
func printMultiplicationTable(n) {
    print("=== " + str(n) + "단 ===")
    for let i = 1; i <= 9; i = i + 1 {
        print(str(n) + " x " + str(i) + " = " + str(n * i))
    }
}

// 7단 출력
printMultiplicationTable(7)
