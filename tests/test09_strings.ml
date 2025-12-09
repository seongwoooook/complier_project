// Test 9: 문자열 연산
// 목적: 문자열 생성, 연결, 인덱싱, 반복 테스트
// 기대 결과: 문자열 연산이 올바르게 동작함

print("=== 문자열 테스트 ===")

// 문자열 생성
let str1 = "Hello"
let str2 = 'World'  // 작은따옴표도 가능
let str3 = "MiniLang"

print("str1:", str1)
print("str2:", str2)
print("str3:", str3)

// 문자열 연결
print("\n--- 문자열 연결 ---")
let greeting = str1 + ", " + str2 + "!"
print(greeting)

let combined = "Hello" + " " + "World"
print(combined)

// 문자열과 다른 타입 연결
print("\n--- 타입 변환 연결 ---")
let num = 42
print("숫자는 " + str(num) + "입니다")

let pi = 3.14159
print("파이 값: " + str(pi))

// 문자열 인덱싱
print("\n--- 문자열 인덱싱 ---")
let word = "ABCDEFG"
print("word:", word)
print("word[0] =", word[0])
print("word[3] =", word[3])
print("word[6] =", word[6])

// 문자열 길이
print("\n--- 문자열 길이 ---")
print("len('Hello') =", len("Hello"))
print("len('') =", len(""))
print("len('MiniLang') =", len("MiniLang"))

// 문자열 반복
print("\n--- 문자열 반복 ---")
let dash = "-"
print("'-' * 10 =", dash * 10)
print("'abc' * 3 =", "abc" * 3)
print("3 * 'xy' =", 3 * "xy")

// 문자열 순회
print("\n--- 문자열 순회 ---")
let text = "HELLO"
let i = 0
while i < len(text) {
    print("문자", i, ":", text[i])
    i = i + 1
}

// 이스케이프 시퀀스
print("\n--- 이스케이프 시퀀스 ---")
let escaped = "탭:\tHello\n새줄 후 텍스트"
print(escaped)

let quote = "He said \"Hello\""
print(quote)

let backslash = "경로: C:\\Users\\Name"
print(backslash)

// 문자열 비교
print("\n--- 문자열 비교 ---")
print("'abc' == 'abc':", "abc" == "abc")
print("'abc' == 'ABC':", "abc" == "ABC")
print("'abc' != 'def':", "abc" != "def")

// 문자열 함수
func repeatString(s, n) {
    let result = ""
    let i = 0
    while i < n {
        result = result + s
        i = i + 1
    }
    return result
}

print("\nrepeatString('ab', 5) =", repeatString("ab", 5))

// 문자 뒤집기
func reverseString(s) {
    let result = ""
    let i = len(s) - 1
    while i >= 0 {
        result = result + s[i]
        i = i - 1
    }
    return result
}

print("reverseString('Hello') =", reverseString("Hello"))
print("reverseString('12345') =", reverseString("12345"))

// 회문 검사
func isPalindrome(s) {
    return s == reverseString(s)
}

print("\nisPalindrome('racecar') =", isPalindrome("racecar"))
print("isPalindrome('hello') =", isPalindrome("hello"))
print("isPalindrome('level') =", isPalindrome("level"))

print("\n=== 테스트 9 완료 ===")
