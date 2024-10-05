from confluent_kafka import Producer
import json
from django.conf import settings

class UserProducer:
    def __init__(self):
        # 配置生产者
        self.producer = Producer({
            'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS
        })

    def delivery_report(self, err, msg):
        """回调函数，确认消息是否成功发送"""
        if err is not None:
            print(f'Message delivery failed: {err}')
        else:
            print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

    def send_user_update(self, user_data):
        """发送 User 信息更新到 Kafka topic"""
        try:
            self.producer.produce(
                settings.KAFKA_USER_TOPIC,
                key=str(user_data['id']),
                value=json.dumps(user_data),
                callback=self.delivery_report
            )
            self.producer.flush()  # 确保消息被推送
        except Exception as e:
            print(f"Failed to send message: {str(e)}")
