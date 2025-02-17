generate-ssl:
	openssl req -new -newkey rsa:2048 -nodes -keyout server.key -out server.csr && \
	openssl x509 -req -in server.csr -signkey server.key -out server.crt

init-tg-client:
	python init_tg_client.py