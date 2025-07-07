FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y mkvtoolnix && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt

ENV ANKICONNECT_HOST=http://host.docker.internal:8765

CMD ["python3", "src/script.py"]
