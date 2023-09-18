import asyncio
import os
import pika
import json
import requests
import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger("pika").setLevel(logging.WARNING)


async def receive_into_treatment_queue():
    credentials = pika.PlainCredentials(os.getenv("RABBITMQ_USER"), os.getenv("RABBITMQ_PASSWORD"))
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(os.getenv("RABBITMQ_HOST"), int(os.getenv("RABBITMQ_PORT")), '/', credentials)
    )
    channel = connection.channel()
    channel.queue_declare(queue='treatment')

    def callback(ch, method, properties, body):
        try:
            body = json.loads(body)
            logging.info(f'Received treatment: {body}')
            response = requests.post(f"{os.getenv('BACKEND_URL')}/treatment/", json=body)
            if response.status_code == 201:
                ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            logging.error(e, exc_info=True)

    channel.basic_consume(queue='treatment', on_message_callback=callback, auto_ack=False)
    channel.start_consuming()


if __name__ == '__main__':
    asyncio.run(receive_into_treatment_queue())

