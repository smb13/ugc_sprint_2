#!make
.PHONY: client

include ./.env

DOCKER_COMPOSE = --env-file ./.env -f ./docker-compose.yml

# Default, Help

default: up

help: # Вывод информации make командах
	@grep -E '^[a-zA-Z0-9 _-]+:.*#' Makefile | while read -r l; \
	do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

# Start, First start

up: up_postgres up_mongo up_client # Запуск

up_postgres: # Запуск Postgresql DB
	docker compose $(DOCKER_COMPOSE) up -d postgres

up_mongo: # Запуск Mongo DB
	docker compose $(DOCKER_COMPOSE) up -d mongocfg1 mongors1n1 mongos1

up_client: # Запуск Mongo DB
	docker compose $(DOCKER_COMPOSE) up -d --build --force-recreate client

first_start: first_start_mongo first_start_postgres # Первый запуск

first_start_mongo: up_mongo mongo_config_config mongo_config_shards mongo_config_routers # Первый запуск Mongo DB

first_start_postgres: up_postgres postgres_create_db # Первый запуск Postgresql DB

# Configuration

mongo_config_config: # Конфигурация серверов конфигурации
	docker compose $(DOCKER_COMPOSE) exec -it mongocfg1 bash -c 'echo "rs.initiate({_id: \"mongors1conf\", configsvr: true, members: [{_id: 0, host: \"mongocfg1\"}]})" | mongosh'

mongo_config_shards: # Конфигурация шардов
	docker exec -it mongors1n1 bash -c 'echo "rs.initiate({_id: \"mongors1\", members: [{_id: 0, host: \"mongors1n1\"}]})" | mongosh'

mongo_config_routers: # Конфигурация роутеров
	docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors1/mongors1n1\")" | mongosh'

postgres_create_db: # Создание базы данных
	docker compose $(DOCKER_COMPOSE) exec -it postgres bash -c "/etc/wait-for-postgres.sh localhost && "\
	"echo \"SELECT 'CREATE DATABASE $(POSTGRES_DB)' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = "\
	"'$(POSTGRES_DB)')\gexec\" | psql -U $(POSTGRES_USER)"

# Logs

logs_mongo: # Журнал Mongo
	docker compose $(DOCKER_COMPOSE) logs --tail 100 -f mongocfg1 mongors1n1 mongos1

logs_postgres: # Журнал Postgresql
	docker compose $(DOCKER_COMPOSE) logs --tail 100 -f postgres

logs_client: # Журнал Client
	docker compose $(DOCKER_COMPOSE) logs --tail 100 -f client

# Stop & Down

stop: # Остановка
	docker compose $(DOCKER_COMPOSE) stop

stop_client: # Остановка тестового клиента
	docker compose $(DOCKER_COMPOSE) stop

down: # Удаление
	docker compose $(DOCKER_COMPOSE) down --remove-orphans
