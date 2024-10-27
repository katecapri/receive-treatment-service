#  Сервис по приему обращений #

![](https://github.com/katecapri/images-for-readme/blob/main/tornado.jpeg) ![](https://github.com/katecapri/images-for-readme/blob/main/docker.png)
  ![](https://github.com/katecapri/images-for-readme/blob/main/RabbitMQ.png)


##  Описание ##

Через форму на сайте пользователь оставляет обращение, указывая свою фамилию, имя, отчество, контактный номер телефона и текст обращения. 

После отправки информации пользователем данные попадают в брокер очередей. Из очереди сообщение отправляется на бекенд на фреймворке Tornado, где 
сообщение записывается в базу данных, после чего сохраняется xlsx файл со всеми обращениями, доступ к которому доступен из папки /src/docker/treatment-service. Папку назначения можно заменить в файле docker-compose.yaml в 63й строке.

##  Используемые технологии ##

- Python 3.10
- Docker
- Postgres
- RabbitMQ
- Flask==2.0.2
- Jinja2==3.0.3
- pika==1.3.1
- tornado==6.2
- pandas==1.5.2
- openpyxl==3.0.10
- SQLAlchemy==2.0.15
- psycopg2==2.9.7
- requests==2.28.1


##  Инструкция по развертыванию ##

1. Из папки с проектом ввести команду:

> make treatment-service-run

Либо:

> 	docker network create treatment_network
> 
> 	mkdir -p /src/docker/treatment-service/
> 
> 	docker build -t treatment_db_image -f db.Dockerfile .
> 
> 	docker build -t treatment_frontend_image -f frontend.Dockerfile .
> 
> 	docker build -t treatment_consumer_image -f consumer.Dockerfile .
> 
> 	docker build -t treatment_backend_image -f backend.Dockerfile .
> 
> 	docker-compose -f docker-compose.yaml up -d

2. Просмотр запущенных контейнеров:

> docker ps

![](https://github.com/katecapri/images-for-readme/blob/main/001.png)


##  Результат ##

- По адресу <http://127.0.0.1:5000/> открывается форма для подачи сообщения.

![](https://github.com/katecapri/images-for-readme/blob/main/003.png)

- После отправки обращения по адресу <http://127.0.0.1:8888/> выводится сообщение об отправке.

![](https://github.com/katecapri/images-for-readme/blob/main/004.png)

- По пути /src/docker/treatment-service доступны сохраняемые xlsx файлы.

![](https://github.com/katecapri/images-for-readme/blob/main/005.png)
