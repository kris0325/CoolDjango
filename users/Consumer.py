from confluent_kafka import Consumer, KafkaError
import json
from django.conf import settings
from users.models import User


class UserConsumer:
    def __init__(self):
        # 配置消费者
        self.consumer = Consumer(
            {
                "bootstrap.servers": settings.KAFKA_BOOTSTRAP_SERVERS,
                "group.id": "user_group",
                "auto.offset.reset": "earliest",
            }
        )
        # 订阅 Kafka topic
        self.consumer.subscribe([settings.KAFKA_USER_TOPIC])

    def consume_messages(self):
        """开始消费 Kafka 消息"""
        try:
            while True:
                msg = self.consumer.poll(1.0)  # 等待消息
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue  # 继续等待消息
                    else:
                        print(f"Consumer error: {msg.error()}")
                        continue
                # 处理消息
                user_data = json.loads(msg.value().decode("utf-8"))
                self.update_user_in_db(user_data)
        except Exception as e:
            print(f"Error consuming messages: {str(e)}")
        finally:
            self.consumer.close()

    def update_user_in_db(self, user_data):
        """根据消费的消息更新数据库"""
        try:
            user = User.objects.get(id=user_data["id"])
            user.name = user_data.get("name", user.name)
            user.email = user_data.get("email", user.email)
            user.salary = user_data.get("salary", user.salary)
            user.save()
        except User.DoesNotExist:
            print(f"User with ID {user_data['id']} does not exist.")
