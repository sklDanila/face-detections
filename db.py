import sqlite3

db_file = 'users.db'

# Создаем базу данных SQLite и таблицу users при запуске приложения
def create_db():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            picture BLOB,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_admin INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# Функция для добавления нового пользователя в базу данных
def add_user(username, email, password, picture=None, is_admin=0):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, email, password, picture, is_admin) VALUES (?, ?, ?, ?, ?)', (username, email, password, picture, is_admin))
    conn.commit()
    conn.close()

# Функция для получения пользователя по имени пользователя
def get_user_by_username(username):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user

# Функция для получения пользователя по идентификатору
def get_user_by_id(user_id):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id=?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

# Функция для получения всех пользователей
def get_all_users():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return users

# Функция для получения пользователя по email
def get_user_by_email(email):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email=?', (email,))
    user = cursor.fetchone()
    conn.close()
    return user

# Функция для обновления изображения профиля пользователя
def update_user_picture(user_id, picture_data):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET picture=? WHERE id=?', (picture_data, user_id))
    conn.commit()
    conn.close()


create_db()  # Создаем базу данных при запуске приложения
