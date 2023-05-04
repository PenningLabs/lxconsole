FROM python:3.10.6

RUN mkdir -p /opt/lxconsole
ADD lxconsole /opt/lxconsole/lxconsole
COPY requirements.txt /opt/lxconsole/requirements.txt
COPY run.py /opt/lxconsole/run.py

RUN pip install --upgrade pip
RUN pip3 install -r /opt/lxconsole/requirements.txt

RUN apt update
RUN apt install sqlite3

WORKDIR /opt/lxconsole

ENTRYPOINT [ "python3" ]
CMD [ "run.py" ]