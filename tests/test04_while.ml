// Test 4: while 반복문
// 목적: while 반복문, break, continue 테스트
// 기대 결과: 반복문이 올바르게 실행되고 제어문이 작동함

print("=== while 반복문 테스트 ===")

// 기본 while문
print("1부터 5까지 출력:")
let i = 1
while i <= 5 {
    print(i)
    i = i + 1
}

// 합계 계산
print("\n1부터 10까지의 합:")
let sum = 0
let n = 1
while n <= 10 {
    sum = sum + n
    n = n + 1
}
print("합계:", sum)  // 55

// break 테스트
print("\nbreak 테스트 (5에서 멈춤):")
let j = 1
while j <= 10 {
    if j == 5 {
        print("5를 만나서 중단!")
        break
    }
    print(j)
    j = j + 1
}

// continue 테스트
print("\ncontinue 테스트 (짝수만 출력):")
let k = 0
while k < 10 {
    k = k + 1
    if k % 2 != 0 {
        continue
    }
    print(k)
}

// 중첩 while문
print("\n구구단 2단:")
let row = 1
while row <= 9 {
    print("2 x", row, "=", 2 * row)
    row = row + 1
}

// 카운트다운
print("\n카운트다운:")
let count = 5
while count > 0 {
    print(count)
    count = count - 1
}
print("발사!")

print("\n=== 테스트 4 완료 ===")
