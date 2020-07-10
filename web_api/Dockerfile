FROM python:3.7
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /home/web_api

# Install dependencies
RUN pip install pipenv
COPY Pipfile* /home/web_api/
RUN pipenv install --system
# Copy project
COPY . /home/web_api/
RUN chmod +x /home/web_api/entrypoint.sh

ENTRYPOINT [ "/home/web_api/entrypoint.sh" ]

EXPOSE 8000

