// Example: FizzBuzz
// 프로그래밍 면접의 고전적인 문제

print("=== FizzBuzz ===")
print("1부터 100까지의 숫자를 출력합니다.")
print("3의 배수는 'Fizz', 5의 배수는 'Buzz'")
print("3과 5의 공배수는 'FizzBuzz'를 출력합니다.\n")

func fizzBuzz(n) {
    for let i = 1; i <= n; i = i + 1 {
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
}

// 1부터 30까지 FizzBuzz
fizzBuzz(30)
