"""
Ожидание данных из формы на 8888 хосте.
Пользователю выводится сообщение, что его обращение зарегистрировано.
Данные переводятся в строку, кодируются и направляются в очередь.
"""

import asyncio
import json
import logging

from tornado.web import Application, RequestHandler

from src.treatment.service import save_new_treatment, save_treatments_to_file
from src.message_broker.producer import send_into_treatment_queue

logging.basicConfig(level=logging.INFO)
logging.getLogger("pika").setLevel(logging.WARNING)


class TreatmentReceiveHandler(RequestHandler):

    def post(self):
        try:
            self.set_header("Content-Type", "text/plain")
            treatment_info = dict()
            for param in ["last_name", "first_name", "patronymic", "phone", "treatment"]:
                treatment_info[param] = self.get_argument(param)
            send_into_treatment_queue(json.dumps(treatment_info))
            self.write('Your treatment has been delivered')
        except Exception as e:
            self.write('Error sending treatment')
            logging.error(e, exc_info=True)


class TreatmentSaveHandler(RequestHandler):

    def post(self):
        try:
            treatment = json.loads(self.request.body)
            save_new_treatment(treatment)
            self.set_status(201)
            save_treatments_to_file()
        except Exception as e:
            self.set_status(400)
            logging.error(e, exc_info=True)


async def main():
    app = Application([
        (r"/", TreatmentReceiveHandler),
        (r"/treatment/", TreatmentSaveHandler),
    ])
    app.listen(port=8888)
    shutdown_event = asyncio.Event()
    await shutdown_event.wait()


if __name__ == "__main__":
    asyncio.run(main())(host='0.0.0.0')
