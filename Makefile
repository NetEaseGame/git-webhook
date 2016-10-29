mysql:
	@docker-compose exec mysql mysql -uroot -proot git_webhook
		
build-db:
	@docker-compose exec app python scripts.py build_db
		
