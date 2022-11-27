#  Сервис по приему обращений #


##  Описание ##

Через форму на сайте пользователь оставляет обращение, указывая свою фамилию, имя, отчество, контактный номер телефона и текст обращения. При нажатии на кнопку отправить пользователю выдается текст, что сообщение отправлено. 

После отправки информации пользователем данные попадают в брокер очередей. Информация обрабатывается и записывается в базу данных. После обновления информации в базе формируются 2 файла со всеми обращениями форматов xlsx и csv.

##  Используемые технологии ##

- Python 3.10.2
- Docker
- RabbitMQ==0.2.0
- Flask==2.0.2
- Jinja2==3.0.3
- pika==1.3.1
- tornado==6.2
- pandas==1.5.2
- openpyxl==3.0.10



##  Инструкция по развертыванию ##

1. Загрузка Docker-образа:

> docker pull ekate2212/treatimage

2. Создание Docker-контейнера:

> docker run -d -p 5000:5000 -p 8888:8888 -p 8000:8000 -p 15672:15672 -p 5672:5672 --name treatcont ekate2212/treatimage

3. Просмотр запущенных контейнеров:

> docker ps

![](https://github.com/katecapri/images-for-readme/blob/main/001.png)

4. Запуск bash-консоли внутри контейнера по полученному в предыдущем шаге CONTAINER ID:

> docker exec -it d5234b5e9115 bash

5. Запуск серверов внутри контейнера:

> service rabbitmq-server start

> python3 backend.py & python3 rabbitmq.py

![](https://github.com/katecapri/images-for-readme/blob/main/002.png)




##  Результат ##

- По адресу <http://127.0.0.1:5000/> открывается форма для подачи сообщения.

![](https://github.com/katecapri/images-for-readme/blob/main/003.png)

- После отправки обращения по адресу <http://127.0.0.1:8888/> выводится сообщение об отправке.

![](https://github.com/katecapri/images-for-readme/blob/main/004.png)

- В консоли выводится информация о получении обращения, записи его в БД и формировании файла.

![](https://github.com/katecapri/images-for-readme/blob/main/005.png)

- Полученную информацию также можно посмотреть в терминале приложения Docker Desktop

> ls

> cat treatments.csv

![](https://github.com/katecapri/images-for-readme/blob/main/006.png)

