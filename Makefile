dev-mysql:
	@docker-compose -f docker-compose-dev.yml exec mysql mysql -uroot -proot git_webhook

mysql:
	@docker-compose exec mysql mysql -uroot -proot git_webhook
		
dev-build-db:
	@docker-compose -f docker-compose-dev.yml exec app python scripts.py build_db

build-db:
	@docker-compose exec app python scripts.py build_db
		
