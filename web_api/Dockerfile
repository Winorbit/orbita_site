FROM python:3.7
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
RUN pip install pipenv
COPY Pipfile Pipfile.lock /code/
RUN pipenv install --system
# Copy project
COPY . /code/

EXPOSE 8001

#CMD gunicorn --reload -w 4  -b 0.0.0.0:8001 --env DJANGO_SETTINGS_MODULE=content.settings content.wsgi