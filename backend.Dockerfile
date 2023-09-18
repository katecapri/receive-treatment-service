FROM python:3.10

RUN mkdir /application
WORKDIR /application

COPY backend /application
RUN pip install -r requirements.txt

ENV PYTHONPATH "/application"

RUN chmod +x /application/script.sh
CMD [ "sh", "-c", "/application/script.sh" ]
