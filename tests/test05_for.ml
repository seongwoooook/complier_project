// Test 5: for 반복문
// 목적: for 반복문의 다양한 형태 테스트
// 기대 결과: C 스타일 for문이 올바르게 작동함

print("=== for 반복문 테스트 ===")

// 기본 for문
print("1부터 5까지:")
for let i = 1; i <= 5; i = i + 1 {
    print(i)
}

// 역순 반복
print("\n5부터 1까지 (역순):")
for let i = 5; i >= 1; i = i - 1 {
    print(i)
}

// 증가값 변경
print("\n0부터 10까지 2씩 증가:")
for let i = 0; i <= 10; i = i + 2 {
    print(i)
}

// 팩토리얼 계산
print("\n5! (팩토리얼) 계산:")
let factorial = 1
for let i = 1; i <= 5; i = i + 1 {
    factorial = factorial * i
}
print("5! =", factorial)  // 120

// 중첩 for문 (구구단)
print("\n구구단 2~3단:")
for let i = 2; i <= 3; i = i + 1 {
    print("---", i, "단 ---")
    for let j = 1; j <= 9; j = j + 1 {
        print(i, "x", j, "=", i * j)
    }
}

// for문에서 break
print("\n소수 찾기 (2-20):")
for let num = 2; num <= 20; num = num + 1 {
    let isPrime = true
    for let div = 2; div < num; div = div + 1 {
        if num % div == 0 {
            isPrime = false
            break
        }
    }
    if isPrime {
        print(num, "는 소수")
    }
}

// 합계 with for
print("\n1부터 100까지의 합:")
let total = 0
for let i = 1; i <= 100; i = i + 1 {
    total = total + i
}
print("합계:", total)  // 5050

print("\n=== 테스트 5 완료 ===")
