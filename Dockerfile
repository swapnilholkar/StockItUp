 FROM python:3
 ENV PYTHONUNBUFFERED 1
 RUN mkdir /code
 WORKDIR /code
 ADD requirement.txt /code/
 RUN pip install -r requirement.txt
 ADD . /code/

