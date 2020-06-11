FROM python:3.7
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN /usr/local/bin/python -m pip install --upgrade pip

WORKDIR /home/web_ui/

COPY Pipfile* /home/web_ui/

RUN pip install pipenv && pipenv install --system

EXPOSE 8001