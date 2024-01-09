import sqlite3



class DbSpamer:
    def __init__(self) -> None:
        self.db_path = 'database.db'



    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        return self
    


    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()


    
    def db_add_message_in_messages_admin(self, chat_id, message_id):
        self.cursor.execute("INSERT INTO admin_messages (user_id, message) VALUES (?, ?)", (chat_id, message_id))
        self.conn.commit()
        return True
    


    def db_get_messages_in_chat_admin(self, chat):
        self.cursor.execute("SELECT * FROM admin_messages WHERE user_id = ?", (chat,))
        result = self.cursor.fetchall()
        return result



    def db_delete_message_in_chat_admin(self, chat):
        self.cursor.execute("DELETE FROM admin_messages WHERE user_id = ?", (chat,))
        self.conn.commit()
        return True
    


    def get_all_users(self):
        self.cursor.execute("SELECT * FROM users")
        result = self.cursor.fetchall()
        return result



    def add_user(self, activation_code, end_date):
        self.cursor.execute("INSERT INTO users (activation_code, end_date) VALUES (?, ?)", (str(activation_code), end_date))
        self.conn.commit()
        return True
    


    def get_user_data(self, activation_code):
        self.cursor.execute("SELECT * FROM users WHERE activation_code = ?", (activation_code,))
        result = self.cursor.fetchone()
        return result
    


    def set_hwid_to_user(self, hwid, activation_code):
        self.cursor.execute("UPDATE users SET hwid = ? WHERE activation_code = ?", (hwid, activation_code))
        self.conn.commit()



    def db_check_and_create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            activation_code TEXT,
            adding_date DATE DEFAULT CURRENT_DATE,
            end_date TEXT,
            hwid TEXT
            )''')
        self.conn.commit()
        print("table users was created")


        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS admin_messages (
            user_id INTEGER,
            message TEXT
            )''')
        self.conn.commit()
        print('Table admin_messages was created')



#db.db_path = db_path
#db.db_initialize()