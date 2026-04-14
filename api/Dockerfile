FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Copy dependency manifest from build context root and install
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy full project into the image
COPY . .

# Expose default FastAPI port
EXPOSE 8000

ENV APP_HOST=0.0.0.0 APP_PORT=8000

# Run the FastAPI app. Adjust module path if needed.
CMD ["uvicorn", "llm_module.api:app", "--host", "0.0.0.0", "--port", "8000"]
