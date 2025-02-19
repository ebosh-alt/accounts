generate-ssl:
	openssl req -new -newkey rsa:2048 -nodes -keyout data/server.key -out data/server.csr && \
	openssl x509 -req -in data/server.csr -signkey data/server.key -out data/server.crt

init-tg-client:
	python init_tg_client.py

test_db:
	docker compose --profile dev up --build -d

start:
	python main.py

remove:
	docker compose down db_accounts bot_and_fastapi -v

restart:
	make remove
	make test_db
	make start