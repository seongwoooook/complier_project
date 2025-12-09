// Test 10: 스코프와 클로저
// 목적: 변수 스코프, 함수 스코프, 블록 스코프 테스트
// 기대 결과: 스코프가 올바르게 동작함

print("=== 스코프 테스트 ===")

// 전역 변수
let globalVar = "전역"
print("전역 변수:", globalVar)

// 함수 스코프
func testFunctionScope() {
    let localVar = "지역"
    print("함수 내 지역 변수:", localVar)
    print("함수 내에서 전역 접근:", globalVar)
}

testFunctionScope()
print("함수 외부에서 전역:", globalVar)

// 블록 스코프
print("\n--- 블록 스코프 ---")
let x = 10
print("블록 전 x:", x)

if true {
    let y = 20  // 블록 내 지역 변수
    x = 15      // 외부 변수 수정
    print("블록 내 y:", y)
    print("블록 내 x:", x)
}

print("블록 후 x:", x)

// 중첩 스코프
print("\n--- 중첩 스코프 ---")
let outer = "외부"

func outerFunc() {
    let middle = "중간"
    
    func innerFunc() {
        let inner = "내부"
        print("innerFunc에서 inner:", inner)
        print("innerFunc에서 middle:", middle)
        print("innerFunc에서 outer:", outer)
    }
    
    innerFunc()
    print("outerFunc에서 middle:", middle)
    print("outerFunc에서 outer:", outer)
}

outerFunc()

// 변수 섀도잉
print("\n--- 변수 섀도잉 ---")
let shadow = "전역 shadow"
print("전역:", shadow)

func shadowTest() {
    let shadow = "함수 shadow"
    print("함수 내:", shadow)
    
    if true {
        let shadow = "블록 shadow"
        print("블록 내:", shadow)
    }
    
    print("블록 후:", shadow)
}

shadowTest()
print("함수 후:", shadow)

// 함수 매개변수 스코프
print("\n--- 매개변수 스코프 ---")
let param = "전역 param"

func paramTest(param) {
    print("함수 내 param:", param)
    param = "수정된 param"
    print("수정 후 param:", param)
}

paramTest("인자값")
print("함수 후 전역 param:", param)

// 반복문 스코프
print("\n--- 반복문 스코프 ---")
for let i = 0; i < 3; i = i + 1 {
    let loopVar = i * 10
    print("반복", i, "- loopVar:", loopVar)
}

// 클로저 동작
print("\n--- 클로저 동작 ---")
func makeCounter() {
    let count = 0
    
    func increment() {
        count = count + 1
        return count
    }
    
    return increment
}

// 참고: 현재 MiniLang은 함수를 값으로 반환하는 것을 
// 완전히 지원하지 않으므로 단순 테스트만 수행

func closureDemo() {
    let value = 100
    
    func inner() {
        print("클로저에서 접근한 value:", value)
    }
    
    inner()
    value = 200
    inner()
}

closureDemo()

print("\n=== 테스트 10 완료 ===")
