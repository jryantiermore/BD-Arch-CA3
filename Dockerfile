# latest ver of Dockerfile strengthened for folder hierarchy flexibility
FROM python:3.9-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .
COPY inference/ inference/
COPY ingestion/ ingestion/
COPY gocompare/ gocompare/
COPY models/ /models/

ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["python", "app.py"]
