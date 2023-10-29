import json
import pika
import logging
import bson.json_util as json_util

logging.getLogger("pika").setLevel(logging.ERROR)


class Emit:
    def send(self, id, action, payload):
        self.connect()
        self.publish(id, action, payload)
        self.close()

    def connect(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="tarea_u4_message_broker")
        )

        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange="users", exchange_type="topic")

    def publish(self, id, action, payload):
        routing_key = f"user.{action}.{id}"
        message = json_util.dumps(payload)

        self.channel.basic_publish(
            exchange="users", routing_key=routing_key, body=message
        )

    def close(self):
        self.connection.close()


class Receive:
    def __init__(self):
        logging.info("Waiting for messages...")
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="tarea_u4_message_broker")
        )

        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange="users", exchange_type="topic")

        self.channel.queue_declare("user_for_user_queue", exclusive=True)
        self.channel.queue_bind(
            exchange="users",
            queue="user_for_user_queue",
            routing_key="user.delete.*",
        )

        self.channel.basic_consume(
            queue="user_for_user_queue", on_message_callback=self.callback
        )

        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        body = json.loads(body)
        logging.info(f"Good by {body['name']} 👋")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def close(self):
        self.connection.close()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s:%(levelname)s:%(name)s:%(message)s"
    )
    Receive()