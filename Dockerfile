# updated ver of the Dockerfile after finishing build out of most of pipeline
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies (Pillow, skimage, OpenCV-lite)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["python", "app.py"]
