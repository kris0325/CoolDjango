from abc import ABC, abstractmethod


class CommunicationException(Exception):
    pass


class Caller:
    def __init__(self, name):
        self.name = name


class CommsHandlerABC(ABC):
    @abstractmethod
    def connect(self, user1, user2):
        pass

    @abstractmethod
    def hangup(self, user1, user2):
        pass

    @abstractmethod
    def clear_all(self):
        pass


class CommsHandler(CommsHandlerABC):
    def __init__(self):
        # 初始化 active_connections 为一个列表,里面存储元素为元组(user1, user2)...
        self.active_connections = []

    def connect(self, user1: Caller, user2: Caller) -> str:
        if user1 == user2:
            raise CommunicationException(
                f"{user1.name} cannot connect with {user2.name}"
            )

        # 检查是否已有连接
        if len(self.active_connections) > 0:
            raise CommunicationException("Connection in use. Please try later")

        # 建立连接并加入 active_connections
        self.active_connections.append((user1, user2))
        return f"Connection established between {user1.name} and {user2.name}"

    def hangup(self, user1: Caller, user2: Caller) -> str:
        if user1 == user2:
            raise CommunicationException(
                f"{user1.name} cannot hangup with {user2.name}"
            )

        # 检查连接是否存在并移除
        if (user1, user2) in self.active_connections or (
            user2,
            user1,
        ) in self.active_connections:
            if (user1, user2) in self.active_connections:
                self.active_connections.remove((user1, user2))
            else:
                self.active_connections.remove((user2, user1))
        return f"{user1.name} and {user2.name} are disconnected"

        raise CommunicationException(
            f"{user1.name} and {user2.name} not found in the communication channel"
        )

    def clear_all(self) -> None:
        # 清空所有连接
        self.active_connections = []


# 示例
hana = Caller("Hana")
luca = Caller("Luca")
lev = Caller("Lev")

handler = CommsHandler()

try:
    print(
        handler.connect(hana, luca)
    )  # 输出: Connection established between Hana and Luca
    print(handler.hangup(hana, luca))  # 输出: Hana and Luca are disconnected
    print(
        handler.connect(hana, lev)
    )  # 输出: Connection established between Hana and Lev
    print(
        handler.hangup(luca, lev)
    )  # 抛出异常: Luca and Lev not found in the communication channel
except CommunicationException as e:
    print(e)

"""
元组的顺序区分：

1.在 Python 中，(user1, user2) 和 (user2, user1) 是不同的对象。
如果 self.active_connections 中存储的是 (user1, user2)，直接查找 (user2, user1) 会失败，因为它们不相等。
连接的对称性：

2.通常在通信场景中，连接是对称的，即 (user1, user2) 和 (user2, user1) 表示同一个连接。
但在实现中，如果仅存储一个方向的元组（如 (user1, user2)），hangup 方法需要检查两种顺序，以确保用户无论按哪个顺序调用都能正确断开连接。
"""


"""
在您提供的代码中，异常处理机制通过 `raise` 和 `try-except` 语句实现。这种机制用于处理程序中的错误或异常情况，以确保程序能够优雅地应对问题而不会崩溃。以下是对该机制的详细解释：

## 异常处理机制

### 1. 自定义异常类
```python
class CommunicationException(Exception):
    pass
```
- **定义**：这里定义了一个名为 `CommunicationException` 的自定义异常类，继承自 Python 的内置 `Exception` 类。这个类可以用于表示与通信相关的特定错误。

### 2. 使用 `raise`
在 `CommsHandler` 类的 `connect` 和 `hangup` 方法中，使用了 `raise` 语句来引发异常：
```python
if user1 == user2:
    raise CommunicationException(f"{user1.name} cannot connect with {user2.name}")
```
- **功能**：当用户尝试连接自己或在连接已存在的情况下调用连接方法时，程序会通过 `raise` 语句抛出一个 `CommunicationException` 异常。这会立即终止当前方法的执行，并将控制权转移到调用该方法的地方。

### 3. 使用 `try-except`
在示例代码中，使用了 `try-except` 块来捕获和处理异常：
```python
try:
    print(handler.connect(hana, luca))
    print(handler.hangup(hana, luca))
    print(handler.connect(hana, lev))
    print(handler.hangup(luca, lev))
except CommunicationException as e:
    print(e)
```
- **功能**：在 `try` 块中，程序尝试执行多个方法。如果在这些方法中抛出了 `CommunicationException` 异常，程序会跳转到相应的 `except` 块，并执行其中的代码。
- **输出**：如果发生异常，异常信息将被捕获并打印出来，而不是让程序崩溃。

## 总结
这种异常处理机制使得程序能够：
- 清晰地定义和抛出特定类型的错误（如通信错误）。
- 在出现错误时，通过捕获和处理异常来保持程序的稳定性。
- 提供用户友好的错误信息，而不是让整个程序停止运行。

通过这种方式，开发者可以更好地控制程序的流向和错误处理逻辑，使得代码更加健壮和可维护。
"""

"""
在这段面试代码中，面试官可能希望考察面试者以下几个方面的能力和知识点：

### 1. **异常处理**
- **自定义异常**：面试者需要理解如何创建和使用自定义异常类（如 `CommunicationException`），以及在何种情况下抛出异常。
- **使用 `try-except`**：考察面试者对 `try-except` 语句的理解，如何捕获异常并处理它们，以确保程序的稳定性。

### 2. **面向对象编程**
- **抽象类和方法**：通过 `CommsHandlerABC` 类，面试官可以评估面试者对抽象类和抽象方法的理解，以及如何实现这些方法。
- **类的构造与继承**：考察对类的初始化、属性管理（如 `active_connections`）以及如何通过继承来扩展功能的能力。

### 3. **逻辑思维与问题解决**
- **连接逻辑**：面试者需要展示他们如何处理连接逻辑，例如避免用户连接自己或在已有连接时建立新连接的情况。
- **条件判断**：代码中包含多个条件判断，面试者需要展示他们如何合理地组织这些判断以实现预期功能。

### 4. **数据结构与算法**
- **列表操作**：考察面试者对列表的操作能力，如添加、删除元素等。
- **元组的使用**：通过 `(user1, user2)` 的元组存储连接，评估对元组的理解及其不可变特性。

### 5. **代码风格与可读性**
- **代码组织**：评估面试者在编写代码时是否遵循良好的编码规范，例如命名约定、注释和代码结构。
- **错误处理信息**：考察面试者是否能够提供清晰、易于理解的错误信息，以便于调试和用户反馈。

### 6. **边界情况处理**
- **连接状态管理**：考察面试者如何处理边界情况，例如在没有活跃连接时调用 `hangup` 方法时的行为。

通过这些考察点，面试官能够全面评估应聘者在 Python 编程、异常处理、面向对象设计及逻辑思维等方面的能力。

"""


"""
要优化上述代码以应对并发场景，可以考虑以下几个方面：

## 1. 使用多线程或多进程
由于 Python 的全局解释器锁（GIL）限制了多线程的并行执行，尤其是在 CPU 密集型任务中，因此可以考虑以下方法：

- **多线程**：适用于 I/O 密集型任务，例如网络请求或文件操作。可以使用 `threading` 模块来创建多个线程处理连接请求。
  
- **多进程**：适用于 CPU 密集型任务。使用 `multiprocessing` 模块可以创建多个独立的进程，充分利用多核 CPU。

```python
from multiprocessing import Process

def handle_connection(user1, user2):
    # 处理连接的逻辑
    pass

process = Process(target=handle_connection, args=(user1, user2))
process.start()
```

## 2. 使用异步编程
利用 Python 的 `asyncio` 库可以实现异步 I/O 操作，避免阻塞主线程，从而提高并发处理能力。通过 `async/await` 语法，可以更高效地处理大量并发请求。

```python
import asyncio

async def connect_async(user1, user2):
    # 异步连接逻辑
    await asyncio.sleep(1)  # 模拟 I/O 操作

async def main():
    tasks = [connect_async(hana, luca), connect_async(hana, lev)]
    await asyncio.gather(*tasks)

asyncio.run(main())
```

## 3. 使用锁机制
在并发环境中，确保对共享资源（如 `active_connections` 列表）的访问是安全的，可以使用 `threading.Lock` 或 `multiprocessing.Lock` 来防止数据竞争。

```python
from threading import Lock

lock = Lock()

def connect(self, user1: Caller, user2: Caller) -> str:
    with lock:
        # 连接逻辑
```

## 4. 优化数据结构
选择合适的数据结构以提高性能。例如，如果需要频繁插入和删除元素，考虑使用 `deque`（双端队列）而不是列表，以提高效率。

```python
from collections import deque

self.active_connections = deque()
```

## 5. 使用缓存技术
在高并发场景中，使用缓存可以减少对数据库或其他资源的压力。例如，可以使用 Redis 等内存数据库来缓存频繁访问的数据。

## 6. 负载均衡
在服务器端实现负载均衡，将请求分配到多个工作节点，以提高系统的吞吐量和响应能力。这可以通过反向代理服务器（如 Nginx）来实现。

## 总结
通过结合使用多线程、多进程、异步编程、锁机制、优化数据结构和缓存技术，可以显著提升 Python 应用程序在高并发场景下的性能和稳定性。这些方法可以根据具体的应用需求灵活组合，以达到最佳效果。

"""
