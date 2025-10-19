FROM python:3-alpine
RUN apk add --no-cache socat
RUN pip install pycryptodome
WORKDIR /app
COPY ctf_secrets.py /app/ctf_secrets.py
COPY main.py /app/main.py
CMD ["socat","TCP-LISTEN:25403,reuseaddr,fork","EXEC:\"python3 /app/main.py\""]
