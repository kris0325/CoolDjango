import os
import platform
from ping3 import ping

"""
- **Ping** 测试的是网络层的连通性，确认目标IP是否可达。
- **Curl** 测试的是应用层的可用性，确认特定URL（包括HTTPS）是否能够正常响应。

要检查网络连接的可用性，可以使用 ping 命令和 curl 命令。虽然它们都可以用来测试网络，但它们的工作方式和目的不同。下面是对这两者的具体实现以及Python示例代码。
1. Ping命令
Ping命令用于检查目标IP地址是否可达。它通过发送ICMP请求包并等待响应来工作。
2. Curl命令
Curl命令用于发送HTTP请求，检查特定URL（包括HTTPS）是否可用。这可以提供更多关于服务状态的信息，比如HTTP状态码。

IP地址与HTTP请求URL的关系
在某些情况下，IP地址和HTTP请求URL可以是相同的。例如，如果你有一个服务器的IP地址，你可以直接访问该IP地址来获取服务。然而，HTTP请求URL通常包含协议（http或https）和路径，而IP地址仅是设备在网络中的标识。

"""


def ping_system(host):
    """使用系统命令进行Ping测试"""
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "4", host]  # Ping 4次
    response = os.system(" ".join(command))

    if response == 0:
        print(f"{host} is reachable (system ping)")
    else:
        print(f"{host} is not reachable (system ping)")


def ping_host(host):
    """使用ping3库进行Ping测试"""
    response_time = ping(host)

    if response_time is not None:
        print(f"{host} is reachable, response time: {response_time} ms (ping3)")
    else:
        print(f"{host} is not reachable (ping3)")


if __name__ == "__main__":
    # 示例：使用域名或IP地址进行测试
    test_host = "www.example.com"  # 可以替换为其他域名或IP地址
    print(f"Testing {test_host} with system ping:")
    ping_system(test_host)  # 使用系统命令进行Ping测试

    print(f"\nTesting {test_host} with ping3:")
    ping_host(test_host)  # 使用ping3库进行Ping测试

    # 示例：使用IP地址进行测试
    ip_address = "192.168.1.1"  # 可以替换为实际的IP地址
    print(f"\nTesting {ip_address} with system ping:")
    ping_system(ip_address)  # 使用系统命令进行Ping测试

    print(f"\nTesting {ip_address} with ping3:")
    ping_host(ip_address)  # 使用ping3库进行Ping测试
