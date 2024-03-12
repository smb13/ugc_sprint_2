# ELK сервис


## Подключение сервисов к ELK

Добавить в docker compose чтобы приложение отправляло логи

```yaml
    logging:
      driver: gelf
      options:
        gelf-address: udp://127.0.0.1:5044
        tag: nginx
```

Изменить:
- `tag` имя своего сервиса
- `127.0.0.1:5044` IP взять из VM яндекса с сервиса ELK, порт оставить


## Настройка сервисов под единый формат логов

Формат логов:

- `'%(asctime)s [%(levelname)s] [in %(filename)s: line %(lineno)d] - "%(message)s"'` - такого формата логов нужно придерживаться для сервисов
- `datefmt="[%Y-%m-%d %H:%M:%S.%f %z]"` - формат даты и времени

Пример установки настроек для логгера

```python
import logging

log_format: str = '%(asctime)s [%(levelname)s] [in %(filename)s: line %(lineno)d] - "%(message)s"'
logging.basicConfig(format=log_format, level=10, datefmt="[%Y-%m-%d %H:%M:%S.%f %z]")
```