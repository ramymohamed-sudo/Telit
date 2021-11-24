
FROM python:latest
RUN apt-get update -y
# RUN apt-get install json -y
RUN python3 -m pip install psycopg2-binary
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# COPY script.sh /script.sh     # this is added on the root

CMD ["python", "./pub_mqtt.py" ]    # CMD ["/script.sh"]
