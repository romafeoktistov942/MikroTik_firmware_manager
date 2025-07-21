# MikroTik Firmware Manager

Инструмент для управления обновлениями прошивки маршрутизаторов MikroTik.

## Обзор

Приложение для автоматизации обновлений прошивки маршрутизаторов MikroTik. Позволяет планировать и управлять обновлениями на нескольких устройствах.

## Требования

- **Сервер**: Linux (Ubuntu 18.04+), Docker 20.10+
- **Ресурсы**: 2 ГБ ОЗУ, 10 ГБ диска, доступ в интернет
- **Сеть**: Доступ к API MikroTik, настроенный брандмауэр

## Установка

```bash
git clone https://github.com/romafeoktistov942/MikroTik_firmware_manager.git
cd MikroTik_firmware_manager
cp dotenv.env .env
# Отредактируйте .env файл
```

## Развертывание

**Docker**:
```bash
docker build -t mikrotik-firmware-manager .
docker run -d mikrotik-firmware-manager
```

**Вручную**:
```bash
pip install -r requirements.txt
python manage.py runserver 0.0.0.0:8000
```

## Зависимости

- Python 3.12+
- Django 5.2.4

## Примеры

**Веб-интерфейс**: http://your-server-ip:8000
