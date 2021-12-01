


FROM schranz/armv7hf-debian-python-scipy:0.0.2

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install vim
RUN mkdir /usr/lib/python3/docker_volume

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade pip
COPY . .

RUN python setup.py install

# FROM arm32v7/python:3

# WORKDIR /usr/src/app

# COPY requirements.txt ./
# # RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# CMD [ "python", "./web_flask.py.py" ]


# FROM balenalib/raspberry-pi-debian-python:latest

# WORKDIR /

# COPY . .
# RUN pip install --no-cache-dir -r requirements.txt

# CMD [ "python", "./web_flask.py" ]

# FROM ramyrr/auto-switches_auto-switch
# # python:latest
# # RUN apt-get update -y
# # WORKDIR /
# # /usr/local/bin/python
# #/var/lib/python/python_installed

# # COPY . .
# # RUN pip install --no-cache-dir -r requirements.txt
  

# CMD ["python", "./web_flask.py" ]    
# # CMD ["/script.sh"]

