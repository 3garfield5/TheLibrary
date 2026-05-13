FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
COPY core/requirements.txt /app/core/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY core/ /app/core
RUN pip install --no-cache-dir /app/core

COPY . /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app/core/src:/app

EXPOSE 8000

CMD ["uvicorn", "api.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
