"""
Получение сообщений из очереди.
Информация декодируется и заносится в базу данных.
После обновления БД формируются 2 файла с расширениями .xlsx и .csv
"""

import csv
import sqlite3

import pandas
import pika


def all_treatments_from_db_to_xlsx(sqlite_connection, cursor):
    cursor.execute("""SELECT * FROM treatments""")
    all_treatments = cursor.fetchall()
    first_names, last_names, patronymics, phones, treatments = [], [], [], [], [],
    rows = 0
    for row in all_treatments:
        first_name, last_name, patronymic, phone, treatment = row
        first_names.append(first_name)
        last_names.append(last_name)
        patronymics.append(patronymic)
        phones.append(phone)
        treatments.append(treatment)
        rows += 1
    data_to_file = pandas.DataFrame({
        'First_name': first_names,
        'Last_name': last_names,
        'Patronymic': patronymics,
        'Phone': phones,
        'Treatments': treatments,
    })
    data_to_file.to_excel('./treatments.xlsx')
    if rows in [11, 12, 13, 14]:
        print(f'{rows} записей выгружены в сформированный файл treatments.xlsx')
    elif rows % 10 in [0, 5, 6, 7, 8, 9]:
        print(f'{rows} записей выгружены в сформированный файл treatments.xlsx')
    elif rows % 10 in [1]:
        print(f'{rows} запись выгружена в сформированный файл treatments.xlsx')
    else:
        print(f'{rows} записи выгружены в сформированный файл treatments.xlsx')


def all_treatments_from_db_to_csv(sqlite_connection, cursor):
    cursor.execute("""SELECT * FROM treatments""")
    all_treatments = cursor.fetchall()
    with open('treatments.csv', 'w') as File:
        writer = csv.writer(File)
        writer.writerow(['First_name', 'Last_name', 'Patronymic', 'Phone', 'Treatments'])
        writer.writerows(all_treatments)


def add_treatment_to_db(treatment):
    try:
        sqlite_connection = sqlite3.connect('./treatment.db')
        cursor = sqlite_connection.cursor()
        try:
            sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS treatments (
                                                first_name VARCHAR NOT NULL,
                                                last_name VARCHAR NOT NULL,
                                                patronymic VARCHAR NOT NULL,
                                                phone VARCHAR NOT NULL,
                                                treatment NVARCHAR NOT NULL);'''
            cursor.execute(sqlite_create_table_query)
            sqlite_connection.commit()
        finally:
            first_name, last_name, patronymic, phone, treatment = \
                (treatment[0], treatment[1], treatment[2], treatment[3], treatment[4])
            sqlite_insert_query = """INSERT INTO treatments
                                                 (first_name, last_name, patronymic, phone, treatment)
                                                 VALUES (?, ?, ?, ?, ?);"""
            cursor.execute(sqlite_insert_query, (first_name, last_name, patronymic, phone, treatment))
            sqlite_connection.commit()
            print("Следующая информация добавлена в БД: ", first_name, last_name, patronymic, phone, treatment)
            cursor.execute("""SELECT * FROM treatments""")
            all_treatments_from_db_to_xlsx(sqlite_connection, cursor)
            all_treatments_from_db_to_csv(sqlite_connection, cursor)
            cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def callback(ch, method, properties, body):
    info_str = body.decode('utf-8')
    info_list = info_str.split('&&&')
    print("Получено новое обращение: ", info_list[:5])
    add_treatment_to_db(info_list)


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
channel = connection.channel()
channel.queue_declare(queue='rabbit')
print('Ожидание новой информации')
channel.basic_consume('rabbit', callback, auto_ack=True)
channel.start_consuming()
