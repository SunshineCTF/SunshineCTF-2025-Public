FROM python:3-alpine

RUN apk add --no-cache socat \
    && pip install --no-cache-dir numpy

WORKDIR /app
COPY main.py /app/main.py

EXPOSE 25201

CMD ["socat", "-t", "600", "-T", "600", "TCP-LISTEN:25201,reuseaddr,fork", "EXEC:python3 /app/main.py"]
