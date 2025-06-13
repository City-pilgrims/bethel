import os
import django
import pymysql
from django.contrib.auth import get_user_model
from django.db.utils import OperationalError, ProgrammingError

# ✅ pymysql을 MySQLdb처럼 사용하게 설정
pymysql.install_as_MySQLdb()


def create_superuser_if_needed():
    if os.environ.get("CREATE_SUPERUSER", "").lower() != "true":
        return

    try:
        # Django ORM 사용 전 초기화
        django.setup()

        User = get_user_model()
        username = os.environ.get("DJANGO_SUPERUSER_NAME", "admin")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "admin1234")

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
