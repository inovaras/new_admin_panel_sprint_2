FROM python:3.10

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UWSGI_PROCESSES=1
ENV UWSGI_THREADS=16
ENV UWSGI_HARAKIRI=240
ENV DJANGO_SETTINGS_MODULE='example.settings'

# Установка зависимостей
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Копирование конфигураций
COPY uwsgi/uwsgi.ini uwsgi.ini
COPY run_uwsgi.sh run_uwsgi.sh

# Копирование исходного кода
COPY . .

# Создание необходимых директорий
RUN mkdir -p /var/www/static/ \
    && mkdir -p /var/www/media/ \
    && mkdir -p /opt/app/staticfiles/ \
    && mkdir -p /opt/app/media/

# Запуск collectstatic
RUN python manage.py collectstatic --noinput

EXPOSE 8000

ENTRYPOINT ["uwsgi", "--strict", "--ini", "uwsgi.ini"]
