import sqlite3
import datetime

connection = sqlite3.connect('bot.db')

sql = connection.cursor()

# Creating table for users
sql.execute('CREATE TABLE IF NOT EXISTS users (tg_id INTEGER, name TEXT, phone_number TEXT, registered_time DATETIME);')

# Checking user if exists in table
def check_user(user_id):
    connection = sqlite3.connect('bot.db')
    sql = connection.cursor()
    
    checker = sql.execute('SELECT tg_id FROM users WHERE tg_id = ?', (user_id,)).fetchone()
    
    if checker:
        return True
    
    else:
        return False
    
def add_user_to_base(user_id, name, phone_number):
    connection = sqlite3.connect('bot.db')
    sql = connection.cursor()
    
    sql.execute('INSERT INTO users VALUES (?,?,?,?);', (user_id, name, phone_number, datetime.datetime.now()))
    
    connection.commit()
    
    
def showing_users():
    connection = sqlite3.connect('bot.db')
    sql = connection.cursor()
    
    users = sql.execute('SELECT name FROM users;').fetchall()
    
    return users
    