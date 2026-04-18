FROM python:3.14

ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY api/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY core/ ./core
RUN pip install --no-cache-dir ./core

COPY infrastructure/ ./infrastructure

COPY api/ ./api

EXPOSE 8000

ENV APP_HOST=0.0.0.0 APP_PORT=8000

CMD ["uvicorn", "api.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
