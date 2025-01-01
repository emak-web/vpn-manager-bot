import mysql.connector

from config_reader import config


class BotDB:

    def __init__(self):
        self.db = mysql.connector.connect(
            host=config.host,
            user=config.mysql_user,
            password=config.password,
            port=config.port,
            database=config.mysql_database
        )
        self.cursor = self.db.cursor()
    
    def reconnect_if_necessary(function):
        def wrapper(self, *args, **kwargs):
            if not self.db.is_connected():
                self.db.reconnect(attempts=1, delay=0)
            return function(self, *args, **kwargs)

        return wrapper
    
    @reconnect_if_necessary
    def add_user(self, username: str, telegram_id: int = 'NULL', fullname: str = 'NULL'):
        if fullname != 'NULL':
            fullname = f"'{fullname}'"
        query = f"INSERT INTO users(username, telegram_id, fullname) VALUES('{username}', {telegram_id}, {fullname})"
        self.cursor.execute(query)

        return self.db.commit()
    
    @reconnect_if_necessary
    def add_user_from_wait_list(self, telegram_id: int, username: str, fullname: str):
        query = f"UPDATE users SET telegram_id = {telegram_id}, fullname = '{fullname}' WHERE username = '{username}'"
        self.cursor.execute(query)

        return self.db.commit()
           
    @reconnect_if_necessary 
    def get_user_data(self, telegram_id: int):
        query = f"SELECT * FROM users WHERE telegram_id = {telegram_id}"
        self.cursor.execute(query)

        return self.cursor.fetchall()[0] 
    
    @reconnect_if_necessary
    def update_user_data(self, telegram_id: int, username: str, fullname: str):
        query = f"UPDATE users SET username = '{username}', fullname = '{fullname}' WHERE telegram_id = {telegram_id}"
        self.cursor.execute(query)
        
        return self.db.commit()

    @reconnect_if_necessary
    def get_user_id_list(self):
        query = f"SELECT telegram_id FROM users WHERE telegram_id IS NOT NULL"
        self.cursor.execute(query)

        result = []

        for user in self.cursor.fetchall():
            result.append(user[0])

        return result

    @reconnect_if_necessary
    def get_wait_list(self):
        query = f"SELECT username FROM users WHERE telegram_id IS NULL"
        self.cursor.execute(query)

        result = []

        for user in self.cursor.fetchall():
            result.append(user[0])

        return result
    
    @reconnect_if_necessary
    def remove_from_wait_list(self, username: str):
        query = f"DELETE FROM users WHERE username = '{username}'"
        self.cursor.execute(query)
        
        return self.db.commit()

    @reconnect_if_necessary
    def get_user_list(self):
        query = f"SELECT * FROM users WHERE telegram_id IS NOT NULL"
        self.cursor.execute(query)

        return self.cursor.fetchall()

    @reconnect_if_necessary
    def get_number_of_configs(self, telegram_id: int):
        query = f"SELECT COUNT(users.id) FROM users JOIN configs ON configs.user_id = users.id WHERE telegram_id = {telegram_id}"
        self.cursor.execute(query)

        return self.cursor.fetchall()[0][0]
    
    @reconnect_if_necessary
    def get_user_configs(self, telegram_id: int):
        query = f"SELECT configs.id, privatekey, ip, file_id FROM configs JOIN users ON configs.user_id = users.id WHERE telegram_id = {telegram_id}"
        self.cursor.execute(query)

        result = []

        for config in self.cursor.fetchall():
            result.append(
                {
                    'id': config[0],
                    'privatekey': config[1],
                    'ip': config[2],
                    'file_id': config[3]
                }
            )

        return result
    
    @reconnect_if_necessary
    def add_file_id(self, config_id: int, file_id: str):
        query = f"UPDATE configs SET file_id = '{file_id}' WHERE id = {config_id}"
        self.cursor.execute(query)
        
        return self.db.commit()
    
    @reconnect_if_necessary
    def get_fillname_list(self):
        query = f"SELECT fullname, telegram_id FROM users"
        self.cursor.execute(query)

        return self.cursor.fetchall()
    
    @reconnect_if_necessary
    def get_user_fullname(self, telegram_id: int):
        query = f"SELECT fullname FROM users WHERE telegram_id = {telegram_id}"
        self.cursor.execute(query)
        
        return self.cursor.fetchall()[0][0]
    
    @reconnect_if_necessary
    def get_username(self, telegram_id: int):
        query = f"SELECT username FROM users WHERE telegram_id = {telegram_id}"
        self.cursor.execute(query)

        return self.cursor.fetchall()[0][0]
    
    @reconnect_if_necessary
    def remove_all_file_ids(self):
        query = f"UPDATE configs SET file_id = NULL"
        self.cursor.execute(query)
        
        return self.db.commit()

    @reconnect_if_necessary
    def get_users_publickeys(self):
        query = f"SELECT publickey, users.fullname, users.username FROM configs JOIN users ON configs.user_id = users.id"
        self.cursor.execute(query)

        return self.cursor.fetchall()


db = BotDB()
