// Test 3: 조건문 (if/else)
// 목적: if, else, else if 조건문 테스트
// 기대 결과: 조건에 따른 올바른 분기 실행

print("=== 조건문 테스트 ===")

// 기본 if문
let score = 85

print("점수:", score)

if score >= 90 {
    print("등급: A")
} else if score >= 80 {
    print("등급: B")
} else if score >= 70 {
    print("등급: C")
} else if score >= 60 {
    print("등급: D")
} else {
    print("등급: F")
}

// 중첩 if문
print("\n중첩 조건문 테스트:")
let age = 25
let hasLicense = true

if age >= 18 {
    print("성인입니다.")
    if hasLicense {
        print("운전 가능합니다.")
    } else {
        print("면허가 필요합니다.")
    }
} else {
    print("미성년자입니다.")
}

// 논리 연산자와 함께 사용
print("\n복합 조건 테스트:")
let temperature = 22
let isRaining = false

if temperature >= 20 and temperature <= 25 and not isRaining {
    print("날씨가 좋아서 야외 활동하기 좋습니다!")
} else {
    print("실내 활동을 추천합니다.")
}

// 숫자의 참/거짓 테스트
print("\nTruthy/Falsy 테스트:")
let num = 0
if num {
    print("num은 truthy")
} else {
    print("num은 falsy (0이므로)")
}

let str = ""
if str {
    print("str은 truthy")
} else {
    print("str은 falsy (빈 문자열이므로)")
}

let nonEmpty = "hello"
if nonEmpty {
    print("nonEmpty는 truthy (값이 있으므로)")
}

print("\n=== 테스트 3 완료 ===")
