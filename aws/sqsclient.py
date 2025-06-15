import boto3
from botocore.config import Config
import logging

# 配置日志记录器
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 配置 Boto3 客户端连接 LocalStack 的 SQS 服务
boto3_config = Config(
    region_name="us-east-1",  # 选择区域，LocalStack 支持所有区域
    signature_version='v4'
)

# 使用虚拟凭证连接 LocalStack 的 SQS 服务
sqs_client = boto3.client(
    "sqs",
    aws_access_key_id="fakeAccessKey",  # 虚拟 AWS Access Key
    aws_secret_access_key="fakeSecretAccessKey",  # 虚拟 AWS Secret Key
    endpoint_url="http://localhost:4566",  # LocalStack 的本地端点
    config=boto3_config
)


# 创建一个 SQS 队列
def create_queue(queue_name):
    logger.info(f"Creating queue: {queue_name}")
    response = sqs_client.create_queue(QueueName=queue_name)
    queue_url = response['QueueUrl']
    logger.info(f"Queue created: {queue_url}")
    return queue_url


# 发送消息到 SQS 队列
def send_message(queue_url, message_body):
    logger.info(f"Sending message to queue {queue_url}: {message_body}")
    response = sqs_client.send_message(
        QueueUrl=queue_url,
        MessageBody=message_body
    )
    logger.info(f"Message sent: {response['MessageId']}")


# 接收消息
def receive_messages(queue_url):
    logger.info(f"Receiving messages from queue: {queue_url}")
    response = sqs_client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=10,  # 一次最多接收10条消息
        WaitTimeSeconds=5  # 可选：等待消息出现（最多20秒）
    )
    messages = response.get("Messages", [])
    if not messages:
        logger.info("No messages received.")
    else:
        for message in messages:
            logger.info(f"Received message: {message['Body']}")
            # 处理完消息后删除它
            sqs_client.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=message['ReceiptHandle']
            )
            logger.info(f"Message deleted: {message['MessageId']}")


if __name__ == "__main__":
    # 队列名称
    queue_name = "test-queue-python"

    # 1. 创建队列
    queue_url = create_queue(queue_name)

    # 2. 发送消息到队列
    send_message(queue_url, "Hello from LocalStack!")
    send_message(queue_url, "Another message")

    # 3. 接收并处理消息
    receive_messages(queue_url)
