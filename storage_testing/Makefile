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

up: up_postgres up_mongo build_client # Запуск

up_postgres: # Запуск Postgresql DB
	docker compose $(DOCKER_COMPOSE) up -d postgres

up_mongo: # Запуск Mongo DB
	docker compose $(DOCKER_COMPOSE) up -d mongocfg1 mongors1n1 mongos1

build_client: # Запуск Mongo DB
	docker compose $(DOCKER_COMPOSE) build client

first_start: first_start_postgres first_start_mongo # Первый запуск

first_start_postgres: up_postgres postgres_drop_db postgres_create_db build_client postgres_populate_db # Первый запуск Postgresql DB

first_start_mongo: up_mongo mongo_config_config mongo_config_shards mongo_config_routers build_client mongo_populate_db # Первый запуск Mongo DB

# Запуск тестов

run_tests: up postgres_run_tests mongo_run_tests

postgres_run_tests: # Запуск тестов на Postgresql DB
	docker compose $(DOCKER_COMPOSE) run -it client python3 ./postgres/postgres_test.py

mongo_run_tests: # Запуск тестов на Mongo DB
	docker compose $(DOCKER_COMPOSE) run -it client python3 ./mongo/mongo_test.py

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
	"'$(POSTGRES_DB)')\gexec\" | psql -U $(POSTGRES_USER) -d postgres"

postgres_drop_db: # Удаление базы данных
	docker compose $(DOCKER_COMPOSE) exec -it postgres bash -c "/etc/wait-for-postgres.sh localhost && "\
	"echo \"SELECT 'DROP DATABASE $(POSTGRES_DB)' WHERE EXISTS (SELECT FROM pg_database WHERE datname = "\
	"'$(POSTGRES_DB)')\gexec\" | psql -U $(POSTGRES_USER) -d postgres"

# Populate Databases

postgres_populate_db: # Заполнение базы данных
	docker compose $(DOCKER_COMPOSE) run -it client python3 ./postgres/postgres_create.py

mongo_populate_db: # Заполнение базы данных
	docker compose $(DOCKER_COMPOSE) run -it client python3 ./mongo/mongo_create.py

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
