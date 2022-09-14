build:
	docker-compose build

run:
	docker-compose up

app_down:
	docker-compose down

db_up:
	python migrations/db_up.py

db_down:
	python migrations/db_down.py