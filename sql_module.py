import sqlite3
import os


def create_table():
    cursor.execute('CREATE TABLE users(user_id INTEGER, user_name TEXT, user_username TEXT, last_data TEXT)')


db_path = os.environ["db_path_fts"]
default_table_name = "users"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

existance = cursor.execute(
    f"""SELECT name FROM sqlite_master WHERE type='table' AND name='{default_table_name}'; """).fetchall()
if not existance:
    create_table()


def db_row_exists(user_id, table=default_table_name):
    #   True if exists False if not

    cursor.execute(f"SELECT 1 FROM {table} WHERE user_id = {user_id}")
    return True if len(cursor.fetchall()) >= 1 else False


def db_select(user_id, column, table=default_table_name):
    cursor.execute(f"SELECT {column} FROM {table} WHERE user_id = {user_id}")
    return cursor.fetchall()[0][0]


def db_select_column(column, table=default_table_name):
    cursor.execute(f"SELECT {column} FROM {table}")
    return cursor.fetchall()


def db_update(user_id, column, value, data, table=default_table_name):
    cursor.execute(f"UPDATE {table} SET {column} = ? WHERE user_id = {user_id}", (value,))
    cursor.execute(f"UPDATE {table} SET last_data = ? WHERE user_id = {user_id}", (data,))
    conn.commit()


def db_update_time(user_id, time, table=default_table_name):
    cursor.execute(f"UPDATE {table} SET last_data = ? WHERE user_id = {user_id}", (time,))
    conn.commit()


def db_create_new_row(user_id, name, username, table=default_table_name):

    cursor.execute(f"INSERT INTO {table} (user_id, user_name, user_username)"
                   f" VALUES ({user_id}, ?, ?)", (name, username))
    conn.commit()


