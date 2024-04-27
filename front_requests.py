import requests

BASE_URL = 'http://localhost:5000'


def register_user(username, email, password):
    url = f'{BASE_URL}/register'
    data = {
        'username': username,
        'email': email,
        'password': password
    }
    response = requests.post(url, json=data)
    return response.json()


def login_user(username, password):
    url = f'{BASE_URL}/login'
    data = {
        'username': username,
        'password': password
    }
    response = requests.post(url, json=data)
    return response.json()


def get_user_profile(access_token):
    url = f'{BASE_URL}/profile'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    return response.json()


def upload_user_picture(access_token, image_path):
    url = f'{BASE_URL}/picture/upload'
    headers = {'Authorization': f'Bearer {access_token}'}
    files = {'file': open(image_path, 'rb')}
    response = requests.post(url, headers=headers, files=files)
    return response.json()


def get_users(access_token):
    url = f'{BASE_URL}/users'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    return response.json()


# Пример использования функций:

def main():
    # Регистрация пользователя
    register_response = register_user('example_user', 'example@example.com', 'example_password')
    print(register_response)

    # Вход пользователя
    login_response = login_user('example_user', 'example_password')
    access_token = login_response.get('access_token')

    # Получение профиля пользователя
    profile_response = get_user_profile(access_token)
    print(profile_response)

    # Загрузка изображения профиля
    upload_response = upload_user_picture(access_token, 'path/to/your/image.jpg')
    print(upload_response)

    # Получение списка пользователей (только для администратора)
    users_response = get_users(access_token)
    print(users_response)


if __name__ == '__main__':
    main()
