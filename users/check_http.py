import requests

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


def check_http(url):
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"{url} is reachable and working properly.")
        else:
            print(f"{url} returned an error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


# 示例：使用HTTP URL
check_http("http://192.168.1.1")  # 或者使用 HTTPS


"""
要检查网络连接的可用性，可以使用 `ping` 命令和 `curl` 命令。虽然它们都可以用来测试网络，但它们的工作方式和目的不同。下面是对这两者的具体实现以及Python示例代码。

### 1. Ping命令

**Ping命令**用于检查目标IP地址是否可达。它通过发送ICMP请求包并等待响应来工作。

### 2. Curl命令

**Curl命令**用于发送HTTP请求，检查特定URL（包括HTTPS）是否可用。这可以提供更多关于服务状态的信息，比如HTTP状态码。

### IP地址与HTTP请求URL的关系

在某些情况下，IP地址和HTTP请求URL可以是相同的。例如，如果你有一个服务器的IP地址，你可以直接访问该IP地址来获取服务。然而，HTTP请求URL通常包含协议（http或https）和路径，而IP地址仅是设备在网络中的标识。

### Python Demo

以下是使用Python实现 `ping` 和 `curl` 的示例代码：

#### 1. 使用Python进行Ping测试

```python
import os
import platform

def ping(host):
    # 根据操作系统选择ping命令
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '4', host]  # Ping 4次
    response = os.system(' '.join(command))
    
    if response == 0:
        print(f"{host} is reachable")
    else:
        print(f"{host} is not reachable")

# 示例：使用IP地址
ping("192.168.1.1")
```

#### 2. 使用Python进行HTTP请求测试

```python
import requests

def check_http(url):
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"{url} is reachable and working properly.")
        else:
            print(f"{url} returned an error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

# 示例：使用HTTP URL
check_http("http://192.168.1.1")  # 或者使用 HTTPS
```

### 总结

- **Ping** 测试的是网络层的连通性，确认目标IP是否可达。
- **Curl** 测试的是应用层的可用性，确认特定URL（包括HTTPS）是否能够正常响应。

通过这两个工具，你可以全面了解网络连接的状态。

"""
