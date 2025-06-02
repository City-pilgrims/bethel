FROM python:3.8.6

WORKDIR /home/

# 1. 코드 클론
RUN git clone https://github.com/City-pilgrims/bethel.git

# 2. 작업 디렉토리 이동
WORKDIR /home/bethel_v2/

# ✅ 3. 로컬 .env 파일을 복사
COPY .env /home/bethel_v2/.env

# 4. 의존성 설치
RUN pip install -r requirements.txt

# 5. 포트 오픈 및 실행
EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]