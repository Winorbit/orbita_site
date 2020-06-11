FROM python:3.7
WORKDIR /home/web_ui/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY Pipfile* /home/web_ui/

RUN pip install pipenv && pipenv install --system

EXPOSE 8001