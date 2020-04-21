FROM python:3.7
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


WORKDIR /home/web_ui/

COPY Pipfile Pipfile.lock /home/web_ui/

RUN pip install pipenv && pip install python-logstash && pipenv install --system

EXPOSE 8001

