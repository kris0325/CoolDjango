def leetDecoder(leetText):
    leet_map = {
        '0': 'O', '1': 'I', '2': 'Z', '3': 'E',
        '7': 'T', '#': 'H', '@': 'A', '$': 'S'
    }
    
    words = leetText.split()
    
    def is_leet_word(word):
        return any(char in leet_map for char in word)
    
    result = []
    for word in words:
        if is_leet_word(word):
            decoded_word = ''
            for char in word:
                decoded_word += leet_map.get(char, char)
            result.append(decoded_word.upper())
        else:
            result.append(word.upper())
    
    return ' '.join(result)

# 测试代码
if __name__ == "__main__":
    test_cases = [
        "H3ll0 W0r7d!",
        "#123#",
        "hello world",
        "123 0@#",
        "",
        "H3ll0  W0r7d",
        "@ H 7",
        "h3Ll0 WoR7D"
    ]
    
    for test in test_cases:
        print(f"Input: {test} -> Output: {leetDecoder(test)}")