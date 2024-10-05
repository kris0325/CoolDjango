from django.core.management.base import BaseCommand
from users.Consumer import UserConsumer


class Command(BaseCommand):
    help = 'Starts the Kafka Consumer to listen for user updates'

    def handle(self, *args, **kwargs):
        consumer = UserConsumer()
        consumer.consume_messages()
