# orbita_site

### Работа с докером:
- войти в директорию где лежит docker-compose.yml
- в терминале ввести команду для поднятия контейнеров:
```$ docker-compose up —build -d```
или для поднятия контейнеров в `dev` окружении:
```$ docker-compose -f docker-compose.dev.yml up --build```
- остановить и удалить контейнеры:
```$ docker-compose down```

### Работа с pipenv окружением:
- заинсталить pipenv:
```$ pip install pipenv```
- зайти в директорию конкретного проекта web_api либо web_ui
- поднять окружение:
```$ pipenv shell```
- установить зависимости:
```$ pipenv install```
