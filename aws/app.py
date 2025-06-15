# app.py
from config.sqs_config import SqsConfig
from service.sqs_service import SqsService

if __name__ == "__main__":
    # 1. 获取 SQS 客户端
    sqs_client = SqsConfig.get_sqs_client()

    # 2. 创建 SQS 操作服务
    sqs_service = SqsService(sqs_client)

    # 3. 创建队列
    queue_name = "test-queue"
    queue_url = sqs_service.create_queue(queue_name)

    # 4. 发送消息
    sqs_service.send_message(queue_url, "Hello from LocalStack!")
    sqs_service.send_message(queue_url, "Another message")

    # 5. 接收并处理消息
    sqs_service.receive_messages(queue_url)
