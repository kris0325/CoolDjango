import heapq
from collections import OrderedDict, Counter
from functools import cmp_to_key
from typing import Any


####
# 1 给定一个字符串找出其中出现次数最多的字符 如果出现次数一样多返回最先出现的那个
# 举个栗子：输入helloworld输出l；输入aaabbbcc输出a
#####
]

    def findmostfrequentcharv3(self, s: str) -> Any | None:
        if not s:
            return None

        char_count = Counter(s)

        def compare(item1, item2):
            # 首先比較計數（降序）
            if item1[1] != item2[1]:
                return item2[1] - item1[1]
            # 如果計數相同，按字符的字典序排序（升序）
            return ord(item1[0]) - ord(item2[0])

        # 使用 cmp_to_key 將比較函數轉換為鍵函數
        pq = [cmp_to_key(compare)(item) for item in char_count.items()]
        heapq.heapify(pq)

        # 返回堆頂元素的字符（最頻繁出現的字符）
        return heapq.heappop(pq).obj[0]

# 分析两个solution的时间复杂度和空间复杂度:
#
# 1. OrderedDict解决方案:
# 时间复杂度: O(n)，其中n是字符串长度。遍历字符串一次统计频率，然后遍历OrderedDict找出最大值。
# 空间复杂度: O(k)，其中k是不同字符的数量，最坏情况下k=n。
#
# 2. PriorityQueue解决方案:
# 时间复杂度: O(n + k log k)，其中n是字符串长度，k是不同字符的数量。统计频率O(n)，建堆O(k)，取堆顶O(log k)。
# 空间复杂度: O(k)，用于存储字符频率和优先队列。
#
# 在面试中，更推荐PriorityQueue的解决方案，原因如下:
#
# 1. 效率更高: 对于大规模数据，特别是当不同字符数量远小于字符串长度时(k << n)，PriorityQueue方案的时间复杂度优势更明显。
#
# 2. 展示算法知识: 使用优先队列展示了对高级数据结构的理解和应用能力，这在面试中是加分项。
#
# 3. 扩展性好: 如果需要找出前K个高频字符，PriorityQueue方案可以轻松扩展，而OrderedDict方案则需要额外排序。
#
# 4. 空间效率: 两种方案的空间复杂度相同，但PriorityQueue在实际应用中可能更节省空间，因为它不需要保存所有字符的顺序信息。
#
# 5. Python 3.7+兼容性: 由于Python 3.7+的dict已经保证插入顺序，使用OrderedDict的必要性降低，而PriorityQueue的解决方案更具普遍适用性。
#
# 总之，PriorityQueue的解决方案在算法效率、知识广度和实用性方面都更胜一筹，更适合在面试中展示你的编程能力。


if __name__ == "__main__":
    solution = Solution()

    # TEST CASE1
    test1 = "helloword"
    res1 = solution.findmostfrequentchar(test1)
    print(f"test1 : input  '{test1}', Result: '{res1}'")

    # TEST CASE1
    test2 = "aaabbbcd"
    res2 = solution.findmostfrequentchar(test2)
    print(f"test2: input '{test2}', resut: '{res2}'")
