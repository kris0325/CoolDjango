import collections


class MyStack:

    def __init__(self):
        self.queue1 = collections.deque()
        self.tmp_queue2 = collections.deque()

    def push(self, x: int) -> None:
        """
        left pop, right push
        push element x to right in  tmp_queue2
        """
        self.tmp_queue2.append(x)
        while self.queue1:
            self.tmp_queue2.append(self.queue1.popleft())
        self.queue1, self.tmp_queue2 = self.tmp_queue2, self.queue1

    def pop(self) -> int:
        return self.queue1.popleft()

    def top(self) -> int:
        return self.queue1[0]

    def empty(self) -> bool:
        return not self.queue1

# Your MyStack object will be instantiated and called as such:
# obj = MyStack()
# obj.push(x)
# param_2 = obj.pop()
# param_3 = obj.top()
# param_4 = obj.empty()
