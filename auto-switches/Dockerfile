

FROM python:latest
RUN apt-get upgrade -y
# RUN apt-get install json -y
WORKDIR /usr/local/bin
#/var/lib/python

COPY . .
RUN pip install --no-cache-dir -r requirements.txt
  

CMD ["python", "./web_flask.py" ]    
# CMD ["/script.sh"]

