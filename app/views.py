"""
Модуль для загрузки файла на MikroTik через FTP.

Содержит:
- upload_to_mikrotik: функцию для отправки файла на устройство MikroTik по FTP.
- upload_firmware: Django view для обработки формы загрузки прошивки.
"""

import ftplib
import os

from django.shortcuts import render
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()


def upload_to_mikrotik(ip, username, password, file_obj, filename, port):
    """
    Загружает файл на MikroTik через FTP.

    :param ip: IP адрес устройства MikroTik
    :param username: логин для FTP
    :param password: пароль для FTP
    :param file_obj: файловый объект (например, request.FILES['firmware_file'])
    :param filename: имя файла для сохранения на устройстве
    :param port: порт FTP (целое число, обычно 2122)
    :return: Кортеж (True, None) при успехе или (False, текст ошибки)
        при ошибке
    """
    try:
        # Создаём FTP-сессию и подключаемся к устройству
        with ftplib.FTP() as ftp:
            ftp.connect(
                ip, port, timeout=10
            )  # Подключение к FTP серверу MikroTik
            ftp.login(username, password)  # Авторизация
            # Загружаем файл на устройство
            ftp.storbinary(f"STOR {filename}", file_obj)
        return True, None  # Успешная загрузка
    except Exception as e:
        # В случае ошибки возвращаем False и текст ошибки
        return False, str(e)


def upload_firmware(request):
    """
    Django view для обработки формы загрузки прошивки.

    Получает IP устройства и файл из формы, проверяет их,
    загружает файл на MikroTik через FTP.
    Возвращает страницу с результатом (успех или ошибка).
    """
    message = None  # Сообщение для пользователя
    message_type = None  # Тип сообщения (Bootstrap: success/danger)
    if request.method == "POST":
        ip = request.POST.get("ip_address")  # IP адрес устройства из формы
        file = request.FILES.get("firmware_file")  # Файл прошивки из формы
        if file:
            # Проверка размера файла (не более 20 МБ)
            if file.size > 20 * 1024 * 1024:
                message = "Размер файла не должен превышать 20 МБ"
                message_type = "danger"
            # Проверка расширения файла (.npk)
            elif not file.name.lower().endswith(".npk"):
                message = "Файл должен иметь расширение .npk"
                message_type = "danger"
            else:
                # Получаем параметры FTP из .env
                port = int(os.getenv("MIKROTIK_FTP_PORT", "2122"))
                username = os.getenv("MIKROTIK_USERNAME")
                password = os.getenv("MIKROTIK_PASSWORD")
                # Загружаем файл на MikroTik
                success, error = upload_to_mikrotik(
                    ip, username, password, file, file.name, port
                )
                if success:
                    message = f"Файл успешно загружен для устройства {ip}!"
                    message_type = "success"
                else:
                    message = f"Ошибка при загрузке файла: {error}"
                    message_type = "danger"
        else:
            # Если файл не выбран
            message = "Файл не выбран"
            message_type = "danger"
    # Возвращаем страницу с сообщением о результате
    return render(
        request,
        "upload.html",
        {"message": message, "message_type": message_type},
    )
