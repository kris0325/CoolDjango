# solution2: 简单迭代法实现  fibobacci func
# def fib(n):
#     """print fibobacci func"""
#     result = []
#     a, b = 0, 1
#     while a < n:
#         result.append(a)
#         print(a, end=" ")
#         a, b = b, a + b
#     return result


# solution1
class FibonacciIterator:
    def __init__(self, n):
        """
        构造函数，初始化最大索引 n，并准备存储 Fibonacci 数列的值。
        :param n: int, 最大的 Fibonacci 数列长度
        """
        self.n = n  # 最大索引
        self.current = 0  # 当前索引
        self.a, self.b = 0, 1  # 初始化 Fibonacci 的前两项

    def __iter__(self):
        """
        返回自身，支持迭代。
        """
        return self

    def __next__(self):
        """
        生成下一个 Fibonacci 数。
        """
        if self.current >= self.n:
            raise StopIteration  # 超过范围后停止迭代
        if self.current == 0:
            self.current += 1
            return self.a  # 返回第一个值 0
        elif self.current == 1:
            self.current += 1
            return self.b  # 返回第二个值 1
        else:
            self.a, self.b = self.b, self.a + self.b  # 更新 Fibonacci 值
            self.current += 1
            return self.b  # 返回新计算的值


# 示例
fib = FibonacciIterator(5)  # 构造 Fibonacci 数列到第 5 项
for num in fib:
    print(num, end=" ")  # 输出 0 1 1 2 3


"""
面试中要求实现 `solution1` 这种方式（即自定义迭代器）而不是简单的 `solution2`（即简单函数实现），主要是为了考察候选人在以下几个方面的能力：

## 1. **面向对象编程（OOP）能力**
- **类的使用**：`solution1` 使用了类和对象的概念，展示了候选人对 OOP 的理解和应用能力。面试官希望看到候选人能够将问题抽象为类，并实现相关的方法。
- **迭代器协议**：通过实现 `__iter__()` 和 `__next__()` 方法，候选人展示了对 Python 迭代器协议的理解。这是 Python 中重要的设计模式之一。

## 2. **代码结构与可读性**
- **可扩展性**：`solution1` 的结构使得未来添加更多功能变得简单，例如可以轻松扩展为生成无限 Fibonacci 数列的迭代器。
- **清晰性**：将逻辑分散到不同的方法中，使得代码更易于理解和维护。面试官可能会关注候选人如何组织代码以提高可读性。

## 3. **异常处理**
- **使用 `StopIteration`**：在 `solution1` 中，使用 `StopIteration` 来控制迭代结束，这是处理迭代器的重要部分。面试官希望候选人能理解并正确实现这一机制。

## 4. **算法思维**
- **理解 Fibonacci 数列**：虽然 Fibonacci 数列的计算相对简单，但实现自定义迭代器需要候选人对数列的生成逻辑有清晰的理解，并能够将其转化为代码。

## 5. **复杂度管理**
- **性能考虑**：虽然 `solution2` 更简单，但可能在处理大数据时不够高效或灵活。面试官可能希望看到候选人在设计解决方案时考虑到性能和内存效率。

## 总结
尽管 `solution1` 的实现比 `solution2` 更复杂，但它展示了更深层次的编程技能，包括 OOP、迭代器协议、异常处理和代码结构等方面。面试官通过这种方式考察候选人的综合能力，尤其是在实际工作中可能遇到的更复杂场景下如何设计和实现解决方案。

"""
