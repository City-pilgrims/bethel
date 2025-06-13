#!/bin/bash
set -e

echo "📌 Django entrypoint 시작"

# SECRET_KEY 설정
export SECRET_KEY=$(cat "${SECRET_KEY_FILE}")

# DB 대기
until nc -z ${DB_HOST:-mariadb} ${DB_PORT:-3306}; do
  echo "⏳ DB를 기다리는 중..."
  sleep 2
done

# 마이그레이션
python manage.py migrate --noinput

# 슈퍼유저 생성
if [ "$CREATE_SUPERUSER" = "true" ]; then
  echo "🔐 슈퍼유저 생성 시도"
  python manage.py shell << END
from django.contrib.auth import get_user_model
import os
User = get_user_model()
username = os.environ.get("DJANGO_SUPERUSER_NAME", "admin")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
with open(os.environ.get("DJANGO_SUPERUSER_PASSWORD_FILE")) as f:
    password = f.read().strip()
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
END
fi

# Gunicorn 실행
exec gunicorn bethel_v2.wsgi:application --bind 0.0.0.0:8000
