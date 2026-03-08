FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir --default-timeout=1000 -r requirements.txt
    
COPY . .

WORKDIR /app/rafiq_project

EXPOSE 8000

CMD ["python","manage.py","runserver","0.0.0.0:8000"]