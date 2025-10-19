FROM python:3-alpine

WORKDIR /opt/chal

RUN apk add --no-cache socat && pip install --no-cache-dir pycryptodome && mkdir -p /opt/chal

COPY relay.py /opt/chal/relay.py
COPY secrets.py /opt/chal/secrets.py
COPY flag.txt /flag

RUN chmod a+rx /opt/chal/relay.py /opt/chal/secrets.py && chmod a+r /flag

EXPOSE 25401

CMD ["socat", "-t", "30", "-T", "30", "TCP-LISTEN:25401,reuseaddr,fork", "EXEC:python3 /opt/chal/relay.py"]
