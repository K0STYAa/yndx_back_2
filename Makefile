build:
	docker-compose build

run:
	docker-compose up

app_down:
	docker-compose down

db_up:
	python3 migrations/db_up.py

db_down:
	python3 migrations/db_down.py

test:
	python3 unit_test.py