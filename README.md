# REST API Yandex Disk System

## Разобранны следующие операции:
- POST:      /imports                   - Импортирт элементов файловой системы
- GET:       /nodes/{id}                - Получение информации об элементе по идентификатору
- DELETE:    /delete/{id}               - Удаление элементов по идентификатору
- GET:       /updates                   - Получение списка **файлов**, которые были обновлены за последние 24 часа включительно

Дополнены тесты для для ручек delete и updates

### Для запуска приложения:

```
make build && make run
```

Если приложение запускается впервые, необходимо применить миграции к базе данных:

```
make db_up
```

Если требуется прекратить работу сервиса или бд:
```
make db_down
make app_down
```

Если требуется протестировать сервис:
```
make test
```

### To do:
1. Добавить ручку /node/{id}/history из доп задач.
2. Соблюдение чистой архитектуры.
3. Увеличить покрытие unit-tests.