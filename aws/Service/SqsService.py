# service/sqs_service.py
import logging


class SqsService:
    """处理与 SQS 交互的服务类"""

    def __init__(self, sqs_client):
        """初始化 SQS 服务，传入配置好的 SQS 客户端"""
        self.sqs_client = sqs_client
        self.logger = logging.getLogger(__name__)

    def create_queue(self, queue_name):
        """创建一个 SQS 队列"""
        self.logger.info(f"Creating queue: {queue_name}")
        response = self.sqs_client.create_queue(QueueName=queue_name)
        queue_url = response['QueueUrl']
        self.logger.info(f"Queue created: {queue_url}")
        return queue_url

    def send_message(self, queue_url, message_body):
        """发送消息到 SQS 队列"""
        self.logger.info(f"Sending message to queue {queue_url}: {message_body}")
        response = self.sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=message_body
        )
        self.logger.info(f"Message sent: {response['MessageId']}")

    def receive_messages(self, queue_url):
        """接收并处理 SQS 队列中的消息"""
        self.logger.info(f"Receiving messages from queue: {queue_url}")
        response = self.sqs_client.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=10,  # 一次最多接收10条消息
            WaitTimeSeconds=5  # 等待消息（最多20秒）
        )
        messages = response.get("Messages", [])
        if not messages:
            self.logger.info("No messages received.")
        else:
            for message in messages:
                self.logger.info(f"Received message: {message['Body']}")
                # 处理完消息后删除它
                self.sqs_client.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=message['ReceiptHandle']
                )
                self.logger.info(f"Message deleted: {message['MessageId']}")
