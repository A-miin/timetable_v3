# timetable_v3
Для запуска проекта установите python версии 3.7 и выше, pip и virualenv

Поссле клонирования перейдите в склонированную папку и вывполните следующие команды:

Создайте виртуальное окружение командой
```bash
python3 -m virtualenv -p python3 venv
```
или
```bash
virtualenv -p python3 venv
```
Активируйте виртуальное окружение командой
```bash
source venv/bin/activate
```

Установите зависимости командой
```bash
pip install -r requirements.txt
```

Перейдите в папку :
```bash
cd timetable_v3
```

Примените миграции командой
```bash
./manage.py migrate
```
или
```bash
python manage.py migrate
```
Загрузите фикстурны командой

```bash
python manage.py loaddata fixtures.json
```

Чтобы запустить сервер выполните:
```bash
python manage.py runserver
```

Для доступа в панель администратора перейдите по ссылке http://localhost:8000/admin

Username для администратора из фикстур: admin, пароль: admin
