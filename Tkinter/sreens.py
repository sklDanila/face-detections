import tkinter as tk
from tkinter import Image, ttk, filedialog, messagebox
from PIL import Image, ImageTk
import requests


class RegistrationScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Register")
        self.root.geometry("500x400")
        self.profile_image = None

        # Левая панель с кнопками
        left_frame = ttk.Frame(self.root)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Кнопка "Логин"
        login_button = ttk.Button(
            left_frame, text="Логин", command=self.show_login_screen
        )
        login_button.pack(pady=10)

        # Кнопка "Регистрация" (активная)
        register_button = ttk.Button(
            left_frame, text="Регистрация", command=self.show_registration_screen
        )
        register_button.pack(pady=10)

        # Правая панель с формой регистрации
        self.right_frame = ttk.Frame(self.root)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # **Форма регистрации**
        # **Имя пользователя**
        username_label = ttk.Label(self.right_frame, text="Имя пользователя:")
        username_label.pack(pady=5)
        self.username_entry = ttk.Entry(self.right_frame)
        self.username_entry.pack(pady=5)

        # **Адрес электронной почты**
        email_label = ttk.Label(self.right_frame, text="Адрес электронной почты:")
        email_label.pack(pady=5)
        self.email_entry = ttk.Entry(self.right_frame)
        self.email_entry.pack(pady=5)

        # **Пароль**
        password_label = ttk.Label(self.right_frame, text="Пароль:")
        password_label.pack(pady=5)
        self.password_entry = ttk.Entry(self.right_frame, show="*")
        self.password_entry.pack(pady=5)

        # **Подтверждение пароля**

        # **Загрузить изображение профиля**
        upload_image_button = ttk.Button(
            self.right_frame, text="Загрузить изображение", command=self.upload_image
        )
        upload_image_button.pack(pady=10)

        # **Кнопка "Зарегистрироваться"**
        register_button = ttk.Button(
            self.right_frame, text="Зарегистрироваться", command=self.register_user
        )
        register_button.pack(pady=20)

    def show_login_screen(self):
        # Скрыть текущую страницу
        self.right_frame.destroy()

        # Создать новую страницу логина
        self.login_screen = LoginScreen(self.root)

    def show_registration_screen(self):
        # Скрыть текущую страницу
        self.right_frame.destroy()

        # Создать новую страницу регистрации
        self.registration_screen = RegistrationScreen(self.root)

    def upload_image(self):
        # Открыть диалоговое окно выбора файла
        filepath = filedialog.askopenfilename(
            initialdir="/",
            title="Выберите изображение профиля",
            filetypes=[("Изображения", "*.jpg *.png *.jpeg *.gif")],
        )

        # Проверить, был ли выбран файл
        if filepath:
            # Загрузить изображение
            image = Image.open(filepath)

            # Сжать изображение до меньшего размера (по желанию)
            resized_image = image.resize((150, 150))

            # Преобразовать изображение в формат PhotoImage
            self.profile_image = ImageTk.PhotoImage(resized_image)

            # Отобразить изображение в лейбле
            if not hasattr(self, "profile_image_label"):
                self.profile_image_label = ttk.Label(self.right_frame)
                self.profile_image_label.pack(pady=10)
            self.profile_image_label.config(image=self.profile_image)

    def register_user(self):
        # Получить данные из формы регистрации
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        # Отправить данные на сервер
        url = 'http://localhost:5000/register'
        data = {'username': username, 'email': email, 'password': password, 'picture': '12'}
        response = requests.post(url, json=data)

        # Проверить ответ от сервера
        if response.status_code == 201:
            messagebox.showinfo("Register", "Вы успешно зарегистрированы!")
        else:
            messagebox.showerror("Register", "Ошибка регистрации. Пожалуйста, попробуйте еще раз.")


class LoginScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Вход")
        self.root.geometry("500x300")

        # Левая панель с кнопками
        left_frame = ttk.Frame(self.root)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Кнопка "Регистрация"
        register_button = ttk.Button(
            left_frame, text="Регистрация", command=self.show_registration_screen
        )
        register_button.pack(pady=10)

        # Правая панель с формой входа
        self.right_frame = ttk.Frame(self.root)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # **Форма входа**
        # **Имя пользователя**
        username_label = ttk.Label(self.right_frame, text="Имя пользователя:")
        username_label.pack(pady=5)
        self.username_entry = ttk.Entry(self.right_frame)
        self.username_entry.pack(pady=5)

        # **Пароль**
        password_label = ttk.Label(self.right_frame, text="Пароль:")
        password_label.pack(pady=5)
        self.password_entry = ttk.Entry(self.right_frame, show="*")
        self.password_entry.pack(pady=5)

        # **Кнопка "Войти"**
        login_button = ttk.Button(
            self.right_frame, text="Войти", command=self.login_user
        )
        login_button.pack(pady=20)

    def show_registration_screen(self):
        # Скрыть текущую страницу
        self.right_frame.destroy()

        # Создать новую страницу регистрации
        self.registration_screen = RegistrationScreen(self.root)

    def login_user(self):
        # Получить данные из формы входа
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Обработать вход пользователя
        # ...

        # Отобразить сообщение об успешном входе
        tk.messagebox.showinfo("Вход", "Вы успешно вошли!")

    def show_login_screen(self):
        # Destroy the current right_frame (of LoginScreen)
        self.root.right_frame.destroy()

        # Create a new RegistrationScreen instance
        self.registration_screen = RegistrationScreen(self.root)


class App:
    def __init__(self):
        root = tk.Tk()
        app = RegistrationScreen(root)
        root.mainloop()


if __name__ == "__main__":
    app = App()
