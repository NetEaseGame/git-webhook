help:
	@echo "mysql|build-db|dev|dev-mysql"

mysql:
	@docker-compose exec mysql mysql -uroot -proot git_webhook
		
build-db:
	@docker-compose exec app python scripts.py build_db
		
dev:
	@docker-compose -f docker-compose-dev.yml up

dev-mysql:
	@mysql -h 127.0.0.1 -uroot -proot git_webhook
