### Структура проекта:
|          |   home    |            |
|:---------|:---------:|-----------:|
|          |   orbita  |            |
|dev       |release    |dev         |
|nginx     |nginx      |nginx       |
|web_api   |web_api    |web_api     |
|web_ui    |web_ui     |web_ui      |

### Работа с докером:
- войти в директорию где лежит docker-compose.yml
- в терминале ввести команду для поднятия контейнеров:  
```$ docker-compose up —build -d```  
или для поднятия контейнеров в **dev** окружении:  
```$ docker-compose -f docker-compose.dev.yml up --build```
- остановить и удалить контейнеры:
```$ docker-compose down```

### Работа с pipenv окружением:
- заинсталить pipenv:
```$ pip install pipenv```
- зайти в директорию конкретного проекта **web_api** либо **web_ui**
- поднять окружение:
```$ pipenv shell```
- установить зависимости:
```$ pipenv install```

### Просмотр логов:
- коннектимся к серверу по ssh:
```$ ssh orbita@31.131.28.206```
- вводим пароль:
```$ ********```
- выбираем проект **dev** либо **release** либо **prod** и интересующий сервис **web_api** либо **web_ui**:  
```$ nano /home/orbita/dev/web_api/api_logfile.log```  
```$ nano /home/orbita/dev/web_ui/ui_logfile.log```
- для просмотра логов **nginx** выбираем проект **dev** либо **release** либо **prod**:  
```$ nano /home/orbita/dev/access.log```  
```$ nano /home/orbita/dev/nginx/error.log```
