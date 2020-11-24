import pymysql.cursors
from contextlib import closing
import json
import datetime
from config import DB_CONFIG
from pprint import pprint


def get_connection():
    connection = pymysql.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database'],
        cursorclass=pymysql.cursors.DictCursor,
    )
    return connection


users_table_name = 'robocontest_bot_users'
attempts_table_name = 'robocontest_bot_attempts'


def insert_user(user_data):
    user_data_keys = tuple(user_data.keys())
    user_data_values = tuple(user_data.values())

    fields = ','.join(user_data_keys)
    mask = ','.join(['%s'] * len(user_data_values))

    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            sql = f'INSERT INTO testdb.{users_table_name} ({fields}) VALUES ({mask})'

            cursor.execute(sql, user_data_values)
            connection.commit()

    return cursor.rowcount


def insert_attempt(attempt_data):
    attempt_data_keys = tuple(attempt_data.keys())
    attempt_data_values = tuple(attempt_data.values())

    fields = ','.join(attempt_data_keys)
    mask = ','.join(['%s'] * len(attempt_data_values))

    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            sql = f'INSERT INTO testdb.{attempts_table_name} ({fields}) VALUES ({mask})'

            cursor.execute(sql, attempt_data_values)
            connection.commit()

    return cursor.rowcount


def get_user(id):
    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT * FROM testdb.{users_table_name} WHERE tg_id = %s OR id = %s', (id, id))
            record = cursor.fetchone()

    return record


def update_user_info(id, **kwargs):
    if 'lang' in kwargs.keys():
        value = kwargs['lang']
        sql = f'UPDATE testdb.{users_table_name} SET lang = %s WHERE tg_id = %s OR id = %s'

    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, (value, id, id))
            connection.commit()

    return_value = 'not updated'

    if connection.affected_rows() != 0:
        return_value = 'updated'

    return return_value
