import os
import pika


def send_into_treatment_queue(treatment_info):
    credentials = pika.PlainCredentials(os.getenv("RABBITMQ_USER"), os.getenv("RABBITMQ_PASSWORD"))
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(os.getenv("RABBITMQ_HOST"), int(os.getenv("RABBITMQ_PORT")), '/', credentials)
    )

    channel = connection.channel()
    channel.queue_declare(queue='treatment')
    channel.basic_publish(exchange='', routing_key='treatment', body=treatment_info)
    connection.close()
