def computeChecksumAggregation(n):
    MOD = 10**9 + 7
    result = 0

    for i in range(1, n):
        # 1. 固定 i 时，i % j = i，出现 n - i 次
        result = (result + 2 * i * (n - i)) % MOD

        # 2. 计算 sum_{j=i+1}^{n} (j % i)
        k = 1
        while k * i <= n:
            l = k * i
            r = min(n, (k + 1) * i - 1)
            count = r - l + 1
            sum_mod = ((l - k * i + r - k * i) * count // 2) % MOD
            result = (result + 2 * sum_mod) % MOD
            k += 1

    return result


# ✅ 测试区
if __name__ == '__main__':
    test_cases = [
        (2, 2),
        (3, 10),
        (4, 24),
        (5, 52),
        (10, 430),
        (100000, 191623417),
    ]

    for n, expected in test_cases:
        output = computeChecksumAggregation(n)
        status = "✅ PASS" if output == expected else "❌ FAIL"
        print(f"n = {n} | output = {output} | expected = {expected} | {status}")
