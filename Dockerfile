# updated ver of the Dockerfile after finishing build out of most of pipeline
FROM python:3.9-slim  # base image for container

WORKDIR /app  # create/set the "app" working dir in the container

# Install system dependencies during image build
# relied on copilot for guidance with this chunk of code
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .  # copy in the requirements into the container
RUN pip install --no-cache-dir -r requirements.txt  # use pip to install packages listed in the file

COPY . .  # copies from VM dir to the container

ENV FLASK_APP=app.py  # tells Flask to use the app.py file I created
ENV PYTHONUNBUFFERED=1  # avoids buffering output files...recommendation discovered

EXPOSE 5000  # port Flask runs on

CMD ["python", "app.py"]  # command run when the containers starts to start app.py
