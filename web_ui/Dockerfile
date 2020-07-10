FROM python:3.7
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


WORKDIR /home/web_ui

COPY Pipfile* /home/web_ui/

RUN pip install pipenv && pipenv install --system

COPY . /home/web_ui/

RUN ./manage.py migrate

EXPOSE 8001

