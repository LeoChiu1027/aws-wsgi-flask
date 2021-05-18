import sqlite3


class UserModel:
    name = ''
    email = ''
    password = ''

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def add_user(self):
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()
        insert_query = 'INSERT INTO users VALUES(?, ?, ?, ?)'
        cursor.execute(insert_query, (None, self.name,
                       self.email, self.password))
        conn.commit()
        conn.close()

    def update_user(self):
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()
        update_query = 'UPDATE users SET name=?, email=?, password=? WHERE id=?'
        cursor.execute(update_query, (self.name,
                                      self.email, self.password, self.id))
        conn.commit()
        conn.close()

    @staticmethod
    def get_user(name):
        user = None
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()
        query_one_query = 'SELECT * FROM users WHERE name=?'
        result = cursor.execute(query_one_query, (name,)).fetchone()
        if result is None:
            return None
        user = UserModel(result[1], result[2], result[3])
        user.id = result[0]
        conn.close()
        return user

    @staticmethod
    def delete_user(name):
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()
        delete_query = 'DELETE FROM users WHERE name=?'
        cursor.execute(delete_query, (name,))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all_user():
        users = []
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()
        query_one_query = 'SELECT * FROM users'
        for item in cursor.execute(query_one_query):
            print(item[1])
            user = UserModel(item[1], item[2], item[3])
            user.id = item[0]
            users.append(user)
        conn.close()
        return users
