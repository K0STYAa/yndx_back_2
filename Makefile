build:
	docker-compose build yndx_back

run:
	docker-compose up yndx_back

app_down:
	docker-compose down yndx_back

migrate:
	migrate -path ./services/files_info/internal/repository/postgres/migrations -database 'postgres://postgres:qwerty@0.0.0.0:49155/postgres?sslmode=disable' up

db_down:
	migrate -path ./services/files_info/internal/repository/postgres/migrations -database 'postgres://postgres:qwerty@0.0.0.0:49155/postgres?sslmode=disable' down