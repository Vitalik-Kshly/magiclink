import sqlite3, os

class DbClient:
    def __init__(self, db_name: str) -> None:
        self.db_name = db_name
        self.db_connection = sqlite3.connect(db_name)
        self.cursor = self.db_connection.cursor()
        self.cursor.execute("SELECT * FROM sqlite_master WHERE type='table' AND name='users'")
        if len(self.cursor.fetchall()):
            pass
        else:
            with open('schema.sql') as f:
                self.db_connection.executescript(f.read())
        self.db_connection.close()

    def add_count(self, key):
        self.db_connection = sqlite3.connect(self.db_name)
        self.cursor = self.db_connection.cursor() 
        self.cursor.execute("SELECT enter_count FROM users WHERE key = ?", (key, ))
        count = str(int(self.cursor.fetchall()[0][0]) + 1)
        self.cursor.execute("UPDATE users SET enter_count = ? WHERE key = ?", (count, key))
        self.db_connection.commit()
        return count

    def get_admin_info(self):
        self.db_connection = sqlite3.connect(self.db_name)
        self.cursor = self.db_connection.cursor()   
        self.cursor.execute("SELECT name, email, enter_count FROM users")
        return self.cursor.fetchall()


    def get_key(self, key: str) -> str:
        '''
        Returns a user name for a 'key'
        '''
    
        self.db_connection = sqlite3.connect(self.db_name)
        self.cursor = self.db_connection.cursor()   
        self.cursor.execute("SELECT name FROM users WHERE key = ?", (key, ))
        return self.cursor.fetchall()
    
    
    
    def check_user(self, email: str) -> bool:
        '''
        Check if there is 'name' user in table 
        '''
        self.db_connection = sqlite3.connect(self.db_name)
        self.cursor = self.db_connection.cursor()   
        self.cursor.execute("SELECT count(1) FROM users WHERE email = ?", (email, ))
        return self.cursor.fetchall()[0][0]

    
    def add_new_user(self, name: str, email: str, key: str) -> None or 1:
        '''
        Add user & key to table
        '''
        if self.check_user(email):
            return None
        self.db_connection = sqlite3.connect(self.db_name)
        self.cursor = self.db_connection.cursor()
        self.cursor.execute("INSERT INTO users VALUES(?,?,?,?)", (name, email, key, 0))
        self.db_connection.commit()
        return 1


    
