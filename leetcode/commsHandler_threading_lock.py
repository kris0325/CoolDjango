import threading

"""
2. 使用锁机制
在多线程环境中，使用锁机制可以确保对共享资源的安全访问。以下是使用 threading 模块实现的代码示例：
"""

"""
在 Python 中，`threading.Lock` 和 `asyncio.Lock` 都用于确保对共享资源的安全访问，但它们的工作机制和适用场景有显著的不同。以下是对这两者的比较，以及在生产环境中选择哪种技术的建议。

## 1. 锁机制的作用

### 类似于 Java 的 `synchronized`
在 Python 中，`threading.Lock` 的作用与 Java 中的 `synchronized` 关键字相似。它们都用于保护临界区，确保同一时间只有一个线程或协程可以访问特定的代码块或资源。通过使用锁，可以防止数据竞争和不一致性的问题。

## 2. `threading.Lock` 与 `asyncio.Lock` 的区别

| 特性                     | `threading.Lock`                               | `asyncio.Lock`                                |
|------------------------|------------------------------------------------|-----------------------------------------------|
| **并发模型**             | 多线程，适用于多线程环境                         | 单线程事件循环，适用于异步编程                     |
| **线程安全**             | 是，适用于多个线程之间的同步                       | 不是，仅适用于协程之间的同步                      |
| **使用场景**             | 适合 I/O 密集型和 CPU 密集型任务                    | 适合 I/O 密集型任务，尤其是需要非阻塞操作时            |
| **性能**                | 由于上下文切换和线程管理开销，性能可能较低            | 更轻量级，避免了线程管理和上下文切换的开销            |
| **锁获取方式**           | 阻塞式获取锁                                      | 非阻塞式获取锁，允许协程在等待时让出控制权              |

## 3. 性能比较
- **`threading.Lock`**：由于涉及到多线程上下文切换和资源管理，性能开销相对较大。在高并发情况下，可能会导致性能下降。
- **`asyncio.Lock`**：由于使用单线程事件循环，并且只在协程之间进行切换，因此性能开销较小，更加高效。

## 4. 适用场景
- **选择 `threading.Lock`**：如果你的应用程序需要处理 CPU 密集型任务或者需要与现有多线程代码兼容，那么使用 `threading.Lock` 是合适的。
- **选择 `asyncio.Lock`**：如果你的应用程序主要处理 I/O 密集型任务（如网络请求、文件 I/O），并且希望利用非阻塞特性以提高并发处理能力，那么使用 `asyncio.Lock` 是更好的选择。

## 5. 在生产环境中的选择
- 对于需要处理大量并发 I/O 操作（如网络爬虫、实时数据处理等）的应用，推荐使用 **`asyncio`**。它能够有效管理大量并发请求，同时减少资源消耗。
- 对于需要执行 CPU 密集型任务或与现有多线程系统集成的应用，则应选择 **`threading`**。虽然 Python 的 GIL 限制了真正的并行执行，但在 I/O 操作中可以释放 GIL，从而提高效率。

总结来说，选择哪种技术应根据具体应用场景、性能需求以及开发团队的熟悉程度来决定。在现代网络应用中，异步编程越来越受到青睐，但多线程仍然在某些特定情况下发挥着重要作用。

"""


"""
在 Python 的 `threading` 模块中，`threading.Lock()` 是用于实现线程间同步的一种机制。它确保在同一时刻只有一个线程能够访问被锁保护的代码区域，从而避免数据竞争和不一致性问题。下面将详细介绍 `acquire()` 和 `release()` 方法与 `try` 块结合的用法，以及使用 `with` 语句的方式。

## 1. 常用语法

### 创建锁
```python
import threading

lock = threading.Lock()  # 创建一个锁对象
```

### 获取锁（acquire）
- **阻塞获取**：默认情况下，调用 `acquire()` 方法会阻塞当前线程，直到获取到锁。
```python
lock.acquire()  # 获取锁
```

- **非阻塞获取**：可以通过设置 `blocking=False` 来尝试获取锁，如果无法立即获取，则返回 `False`。
```python
if lock.acquire(blocking=False):
    try:
        # 访问共享资源
    finally:
        lock.release()  # 确保释放锁
```

- **带超时的获取**：可以设置超时时间，如果在指定时间内未能获取到锁，则返回 `False`。
```python
if lock.acquire(timeout=1):  # 等待最多1秒
    try:
        # 访问共享资源
    finally:
        lock.release()
```

### 释放锁（release）
```python
lock.release()  # 释放锁
```

### 检查锁状态
```python
is_locked = lock.locked()  # 如果锁被某个线程持有，返回 True
```

## 2. 使用 `try` 块结合 `acquire()` 和 `release()`
使用 `try` 块结合 `acquire()` 和 `release()` 的方式，可以确保即使在访问共享资源时发生异常，也能正确释放锁。这是防止死锁的重要措施。

```python
import threading

counter = 0
lock = threading.Lock()

def increment():
    global counter
    for _ in range(1000):
        lock.acquire()  # 获取锁
        try:
            counter += 1  # 修改共享变量
        finally:
            lock.release()  # 确保释放锁

threads = [threading.Thread(target=increment) for _ in range(10)]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

print(f"Final counter value: {counter}")  # 输出最终计数器值
```

## 3. 使用 `with` 语句的方式

使用 `with` 语句可以简化锁的获取和释放过程。`with` 语句会自动调用 `acquire()` 方法来获取锁，并在代码块结束时自动调用 `release()` 方法来释放锁。这种方式不仅简洁，而且更安全，因为它确保了即使发生异常也能正确释放锁。

### 示例代码：
```python
import threading

counter = 0
lock = threading.Lock()

def increment():
    global counter
    for _ in range(1000):
        with lock:  # 自动获取和释放锁
            counter += 1

threads = [threading.Thread(target=increment) for _ in range(10)]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

print(f"Final counter value: {counter}")  # 输出最终计数器值
```

## 总结

- **创建和使用**：使用 `threading.Lock()` 创建一个锁对象，通过 `acquire()` 和 `release()` 方法来控制对共享资源的访问。
- **异常安全**：结合使用 `try...finally` 确保即使发生异常也能正确释放锁。
- **简化语法**：使用 `with` 语句可以简化代码，使得获取和释放锁的过程更加清晰和安全。

这种机制在多线程编程中非常重要，可以有效避免数据竞争和保证数据一致性。

"""


"""
在 Python 的 `threading` 模块中，`with` 语句和 `try` 块结合 `acquire()` 和 `release()` 方法的用法各有其特点和适用场景。下面详细解释这两种方法的区别以及推荐使用的方式。

## 1. `with` 语句的用法

使用 `with` 语句可以自动获取和释放锁，类似于 Java 中的 `synchronized` 关键字。具体来说：

- **自动加锁和解锁**：当进入 `with` 块时，锁会被自动获取；当退出 `with` 块时，无论是正常退出还是由于异常退出，锁都会被自动释放。这种方式确保了即使在代码块中发生异常，也不会导致死锁。

### 示例代码
```python
import threading

lock = threading.Lock()

def critical_section():
    with lock:  # 自动获取锁
        # 执行临界区代码
        print("Lock acquired, executing critical section")

# 创建线程
thread = threading.Thread(target=critical_section)
thread.start()
thread.join()
```

## 2. 使用 `try` 块结合 `acquire()` 和 `release()`

这种方式需要手动调用 `acquire()` 来获取锁，并在 `finally` 块中调用 `release()` 来释放锁。虽然这种方式提供了更大的灵活性，但也更容易出错，例如忘记释放锁可能导致死锁。

### 示例代码
```python
import threading

lock = threading.Lock()

def critical_section():
    lock.acquire()  # 显式获取锁
    try:
        # 执行临界区代码
        print("Lock acquired, executing critical section")
    finally:
        lock.release()  # 确保释放锁

# 创建线程
thread = threading.Thread(target=critical_section)
thread.start()
thread.join()
```

## 3. 哪种方式更推荐？

- **推荐使用 `with` 语句**：因为它简化了代码，使得获取和释放锁的过程更加清晰和安全。使用上下文管理器可以有效避免忘记释放锁的问题，从而减少死锁的风险。

- **使用 `try...finally`**：在某些情况下，如果需要在不同的条件下进行复杂的逻辑处理，或者需要更细粒度的控制，可以选择这种方式。但要确保在所有可能的路径中都能正确释放锁。

## 总结

- 使用 `with lock:` 是一种更安全、更简洁的方法来管理线程同步，自动处理加锁和解锁。
- 使用 `lock.acquire()` 和 `lock.release()` 提供了更大的灵活性，但也增加了出错的风险。
- 在大多数情况下，推荐使用 `with` 语句来处理线程间的同步，以确保代码的可读性和安全性。


"""


class CommunicationException(Exception):
    pass


class Caller:
    def __init__(self, name):
        self.name = name


class CommsHandler:
    def __init__(self):
        self.active_connections = []
        self.lock = threading.Lock()  # 创建锁对象

    def connect(self, user1: Caller, user2: Caller) -> str:
        with self.lock:  # 使用锁确保线程安全
            if user1 == user2:
                raise CommunicationException(
                    f"{user1.name} cannot connect with {user2.name}"
                )

            if len(self.active_connections) > 0:
                raise CommunicationException("Connection in use. Please try later")

            self.active_connections.append((user1, user2))
            return f"Connection established between {user1.name} and {user2.name}"

    def hangup(self, user1: Caller, user2: Caller) -> str:
        with self.lock:  # 使用锁确保线程安全
            if user1 == user2:
                raise CommunicationException(
                    f"{user1.name} cannot hangup with {user2.name}"
                )

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


def main():
    hana = Caller("Hana")
    luca = Caller("Luca")
    lev = Caller("Lev")

    handler = CommsHandler()

    try:
        print(handler.connect(hana, luca))
        print(handler.hangup(hana, luca))
        print(handler.connect(hana, lev))
        print(handler.hangup(luca, lev))  # This will raise an exception
    except CommunicationException as e:
        print(e)


# 运行主函数
main()
