def breakPalindrome(palindromeStr):
    n = len(palindromeStr)

    if n == 1:
        return "IMPOSSIBLE"

    chars = list(palindromeStr)

    for i in range(n // 2):
        if chars[i] != "a":
            chars[i] = "a"
            return "".join(chars)

    # 如果到这里，说明前半部分都是 'a'
    # 如果字符串长度为奇数且中间字符不是 'a'，或者整个字符串都是 'a'，返回 "IMPOSSIBLE"
    if (n % 2 == 1 and chars[n // 2] != "a") or all(c == "a" for c in chars):
        return "IMPOSSIBLE"

    # 否则，将最后一个字符改为 'b'
    chars[-1] = "b"
    return "".join(chars)


# 测试案例
print(breakPalindrome("acca"))  # 输出: "aaca"
print(breakPalindrome("aaa"))  # 输出: "IMPOSSIBLE"
print(breakPalindrome("aba"))  # 输出: "IMPOSSIBLE"
