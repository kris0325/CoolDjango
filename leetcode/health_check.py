import requests
import time
from datetime import datetime

"""
在生产环境中，定期执行健康检查脚本的实现通常涉及将脚本放置在生产实例上，并使用Linux的`cron`作业进行调度。以下是具体的实现步骤：

基于Linux cron 编辑，调度脚本：
crontab -e 
(shared-venv) ➜  ~ crontab -e
crontab: installing new crontab
(shared-venv) ➜  ~
查看脚本
(shared-venv) ➜  ~ crontab -l
* * * * * /usr/local/share/python-venvs/shared-venv/bin/python3 /Users/kris/workspace/workspace/python/CoolDjango/leetcode/health_check.py >> /Users/kris/workspace/workspace/python/CoolDjango/leetcode/log/health_check.log 2>&1
(shared-venv) ➜  ~ python

查看脚本调用日志：
cat /tmp/script_status.log
"""
# 定义要监测的服务URL
service_url = "https://www.google.com/"


def health_check():
    try:
        response = requests.get(service_url)
        # 检查返回状态码
        if response.status_code == 200:
            print("Service is healthy!")
        else:
            print(f"Google Service returned status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Google Service is down! Error: {e}")


if __name__ == "__main__":
    # 在脚本开始时记录时间戳
    with open("/tmp/script_status.log", "a") as f:
        f.write(f"Script started at: {datetime.now()}\n")

    count = 0
    while count < 15:
        health_check()
        count += 1  # 增加计数器
        # 每隔60秒进行一次健康检查
        time.sleep(60)

    # 在脚本结束时记录时间戳
    with open("/tmp/script_status.log", "a") as f:
        f.write(f"Script ended at: {datetime.now()}\n")
