import mysql.connector
from config_reader import config


db = mysql.connector.connect(
    host=config.host,
    user=config.mysql_user,
    password=config.password,
    port=config.port,
)

cursor = db.cursor()

cursor.execute(f'CREATE DATABASE {config.mysql_database}')
cursor.execute(f'USE {config.mysql_database}')
cursor.execute(
    'CREATE TABLE users ('
    'id INT AUTO_INCREMENT PRIMARY KEY,'
    'telegram_id BIGINT,'
    'username VARCHAR(100),'
    'fullname VARCHAR(100)'
    ');'
)
cursor.execute(
    'CREATE TABLE configs ('
    'id INT AUTO_INCREMENT PRIMARY KEY,'
    'user_id INT,'
    'publickey VARCHAR(100),'
    'privatekey VARCHAR(100),'
    'ip VARCHAR(15),'
    'file_id VARCHAR(100),'
    'FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE SET NULL'
    ');'
)
for admin in config.admins:
    cursor.execute(
        f"INSERT INTO users(telegram_id) VALUES({admin})"
    )
    db.commit()

db.close()
