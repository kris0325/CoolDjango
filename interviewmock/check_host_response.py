import requests

# “ Can you use Requests library in Python to send requests to this host
# and print the response if it says....?”
"""
向指定的 URL 发送 HTTP 请求，并检查响应内容是否包含指定的关键字。

参数:
url (str): 目标 URL 地址
keyword (str): 要在响应中搜索的关键字

返回:
None
"""


def check_host_response(url: str, keyword: str) -> None:
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"success{url}")
            if keyword in response.text:
                print(f"响应包含关键字: {keyword}")
            else:
                print(f"响应不包含关键字: {keyword}")
        else:
            print(f"请求失败，状态码:{response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"请求 {url} 时发生错误:{e}")


if __name__ == '__main__':
    url = 'http://www.python.org/'
    keyword = 'python_kris'
    check_host_response(url, keyword)
