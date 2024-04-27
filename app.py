from flask import Flask, request, jsonify, g
import os
import jwt

import db
from db import *

app = Flask(__name__)


# Функция для создания токена доступа
def create_access_token(user_id):
    # В данном примере, предполагается, что вы используете JWT для создания токенов доступа
    return jwt.encode({'user_id': user_id}, 'secret_key', algorithm='HS256')


# Декоратор для проверки аутентификации по токену
def token_required(func):
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'error': 'Необходимо предоставить токен доступа'}), 401

        try:
            data = jwt.decode(token, 'secret_key', algorithms=['HS256'])
            user_id = data['user_id']
            g.user = get_user_by_id(user_id)
            if not g.user:
                return jsonify({'error': 'Неверный токен доступа'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Истек срок действия токена доступа'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Неверный токен доступа'}), 401

        return func(*args, **kwargs)

    return decorated_function


@app.route("/register", methods=['POST'])
def register_user():
    request_data = request.get_json()
    username = request_data.get('username')
    email = request_data.get('email')
    password = request_data.get('password')

    # Проверяем, что переданы все обязательные поля
    if not (username and email and password):
        return jsonify({'error': 'Не передано имя пользователя, email или пароль'}), 400

    # Проверяем, что пользователь с таким именем пользователя или email уже не существует
    if get_user_by_username(username):
        return jsonify({'error': 'Пользователь с таким именем пользователя уже существует'}), 400
    if get_user_by_email(email):
        return jsonify({'error': 'Пользователь с таким email уже существует'}), 400

    # Добавляем пользователя в базу данных
    add_user(username, email, password)

    # В данном примере, просто возвращаем успешный результат без реальной аутентификации
    return jsonify({'message': 'Пользователь успешно зарегистрирован'}), 201


@app.route("/login", methods=['POST'])
def login_user():
    request_data = request.get_json()
    username = request_data.get('username')
    password = request_data.get('password')

    # Проверяем, что переданы все обязательные поля
    if not (username and password):
        return jsonify({'error': 'Не передано имя пользователя или пароль'}), 400

    # Проверяем, что пользователь существует и пароль совпадает
    user = get_user_by_username(username)
    if not user or user[3] != password:
        return jsonify({'error': 'Неверное имя пользователя или пароль'}), 401

    # Создаем токен доступа для пользователя
    access_token = create_access_token(user[0])

    # В данном примере, просто возвращаем успешный результат без реальной аутентификации
    return jsonify({'access_token': access_token}), 200


@token_required
@app.route('/profile', methods=['GET'])
def get_user_profile():
    user_data = {
        'id': g.user[0],
        'username': g.user[1],
        'email': g.user[2],
        'picture': g.user[4],
        'is_admin': bool(g.user[5])
    }
    return jsonify(user_data), 200

@token_required
@app.route('/picture/upload', methods=['POST'])
def upload_user_picture():
    if 'file' not in request.files:
        return jsonify({'error': 'Файл не был загружен'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'Файл не выбран'}), 400

    # Считываем содержимое файла
    file_data = file.read()

    # Обновляем данные о пользователе в базе данных
    update_user_picture(g.user[0], file_data)

    return jsonify({'message': 'Изображение профиля успешно загружено'}), 200


@token_required
@app.route('/users', methods=['GET'])
def get_users():
    if not g.user[5]:  # Проверяем, является ли пользователь администратором
        return jsonify({'error': 'У вас нет прав на просмотр всех пользователей'}), 403

    users = get_all_users()
    return jsonify(users), 200


if __name__ == '__main__':
    app.run(debug=True)
