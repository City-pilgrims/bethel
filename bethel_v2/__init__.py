import os
import django
import pymysql
from django.contrib.auth import get_user_model
from django.db.utils import OperationalError, ProgrammingError

pymysql.install_as_MySQLdb()


def get_password_from_secret():
    file_path = os.environ.get("DJANGO_SUPERUSER_PASSWORD_FILE")
    if file_path and os.path.exists(file_path):
        with open(file_path) as f:
            return f.read().strip()
    return os.environ.get("DJANGO_SUPERUSER_PASSWORD", "admin1234")


def create_superuser_if_needed():
    if os.environ.get("CREATE_SUPERUSER", "").lower() != "true":
        return

    try:
        django.setup()
        User = get_user_model()

        username = os.environ.get("DJANGO_SUPERUSER_NAME", "wlqtk")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
        password = get_password_from_secret()

        if User.objects.filter(username=username).exists():
            print(f"🟢 슈퍼유저 '{username}' 이미 존재함.")
        else:
            print(f"✅ 슈퍼유저 '{username}' 생성 중...")
            User.objects.create_superuser(username=username, email=email, password=password)

    except (OperationalError, ProgrammingError) as e:
        print(f"⚠️ DB 연결 불가 또는 마이그레이션 전 상태: {e}")
    except Exception as e:
        print(f"❌ 슈퍼유저 생성 중 오류: {e}")


create_superuser_if_needed()
