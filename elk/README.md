Добавить в docker compose чтобы приложение отправляло логи

```yaml
    logging:
      driver: gelf
      options:
        gelf-address: udp://127.0.0.1:5044
        tag: nginx
```

