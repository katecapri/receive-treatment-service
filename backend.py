"""
Ожидание данных из формы на 8888 хосте.
Пользователю выводится сообщение, что его обращение зарегистрировано.
Данные переводятся в строку, кодируются и направляются в очередь.
"""

import asyncio

import pika
import tornado.web


class BackApp(tornado.web.RequestHandler):

    def post(self):
        self.set_header("Content-Type", "text/plain")
        treatment_string = ''
        for param in ["last_name", "first_name", "patronymic", "phone", "treatment"]:
            treatment_string += self.get_argument(param) + '&&&'
        send_treatment_to_rabbit_mq(treatment_string.encode('utf-8'))
        self.write('Your treatment has been delivered')


def make_app():
    return tornado.web.Application([
        (r"/", BackApp)])


def send_treatment_to_rabbit_mq(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
    channel = connection.channel()
    channel.queue_declare(queue='rabbit')
    channel.basic_publish(exchange='', routing_key='rabbit', body=message)
    connection.close()


async def main():
    app = make_app()
    app.listen(port=8888)
    shutdown_event = asyncio.Event()
    await shutdown_event.wait()


if __name__ == "__main__":
    asyncio.run(main())(host='0.0.0.0')
