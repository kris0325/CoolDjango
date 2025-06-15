import asyncio

"""
1. 使用异步编程
异步编程适用于处理 I/O 密集型任务，可以有效提高系统的并发处理能力。以下是使用 asyncio 实现的代码示例：
"""


class CommunicationException(Exception):
    pass


class Caller:
    def __init__(self, name):
        self.name = name


class CommsHandler:
    def __init__(self):
        self.active_connections = []

    async def connect(self, user1: Caller, user2: Caller) -> str:
        if user1 == user2:
            raise CommunicationException(
                f"{user1.name} cannot connect with {user2.name}"
            )

        if len(self.active_connections) > 0:
            raise CommunicationException("Connection in use. Please try later")

        # 模拟连接建立的延迟
        await asyncio.sleep(1)
        self.active_connections.append((user1, user2))
        return f"Connection established between {user1.name} and {user2.name}"

    async def hangup(self, user1: Caller, user2: Caller) -> str:
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


async def main():
    hana = Caller("Hana")
    luca = Caller("Luca")
    lev = Caller("Lev")

    handler = CommsHandler()

    try:
        print(await handler.connect(hana, luca))
        print(await handler.hangup(hana, luca))
        print(await handler.connect(hana, lev))
        print(await handler.hangup(luca, lev))  # This will raise an exception
    except CommunicationException as e:
        print(e)


# 运行异步主函数
asyncio.run(main())
