FROM apache/spark:latest

# 将 WordCount.py 和 sample.txt 文件复制到容器中
COPY WordCount.py /opt/spark/
COPY sample.txt /opt/spark/

# 设置工作目录
WORKDIR /opt/spark

# 确保 PATH 包含 Spark 的 bin 目录
ENV PATH="/opt/spark/bin:${PATH}"

# 设置入口点为 Python 脚本
ENTRYPOINT ["spark-submit", "WordCount.py"]