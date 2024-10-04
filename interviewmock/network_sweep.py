import ipaddress
from ping3 import ping
from typing import List


# Can you write a network sweep scanner?
# (basically iterating through a list of IPs and for each do a ping).

def ping_host(ip: str) -> None:
    try:
        response = ping(ip)
        if response is not None:
            print(f"主机 {ip} 可达, 响应时间: {response} 秒")
        else:
            print(f"主机 {ip} 不可达")
    except Exception as e:
        print(f"未知错误: {e}")


def network_sweep(ip_list: List[str]) -> None:
    for ip in ip_list:
        ping_host(ip)


if __name__ == "__main__":
    # 要扫描的 IP 列表
    # ip_list = [str(ip) for ip in ipaddress.IPv4Network("192.168.1.0/30")]
    ip_list = ["192.168.1.1", "192.168.1.2", "192.168.1.3", "192.168.1.8"]

    # 开始网络扫描
    network_sweep(ip_list)
