// Example: 소수 찾기
// 에라토스테네스의 체를 사용한 소수 찾기

print("=== 소수 찾기 ===")

// 소수 판별 함수
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

// n까지의 모든 소수 찾기
func findPrimes(n) {
    let primes = []
    for let i = 2; i <= n; i = i + 1 {
        if isPrime(i) {
            push(primes, i)
        }
    }
    return primes
}

// n번째 소수 찾기
func nthPrime(n) {
    let count = 0
    let num = 1
    while count < n {
        num = num + 1
        if isPrime(num) {
            count = count + 1
        }
    }
    return num
}

// 100까지의 소수
print("\n100 이하의 소수:")
let primesUnder100 = findPrimes(100)
print(primesUnder100)
print("개수:", len(primesUnder100))

// 처음 10개의 소수
print("\n처음 10개의 소수:")
for let i = 1; i <= 10; i = i + 1 {
    print(str(i) + "번째 소수:", nthPrime(i))
}

// 소인수분해
func primeFactors(n) {
    let factors = []
    let d = 2
    while d * d <= n {
        while n % d == 0 {
            push(factors, d)
            n = floor(n / d)
        }
        d = d + 1
    }
    if n > 1 {
        push(factors, n)
    }
    return factors
}

print("\n소인수분해:")
let numbers = [12, 36, 60, 100, 360]
for let i = 0; i < len(numbers); i = i + 1 {
    let n = numbers[i]
    print(str(n) + " =", primeFactors(n))
}
