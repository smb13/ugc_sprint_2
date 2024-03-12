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


Формат логов:

- `'%(asctime)s [%(levelname)s] [in %(filename)s: line %(lineno)d] - "%(message)s"'` - такого формата логов нужно придерживаться для сервисов