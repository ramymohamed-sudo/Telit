

FROM python:latest
RUN apt-get update -y
RUN apt-get install json -y
WORKDIR /var/lib/python

COPY . .
RUN pip install --no-cache-dir -r requirements.txt
# COPY script.sh /script.sh     # this is added on the root

CMD ["python", "./web_flask.py" ]    # CMD ["/script.sh"]

