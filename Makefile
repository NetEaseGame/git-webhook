help:
	@echo "clean|mysql|build-db|dev|dev-mysql"
	
clean:
	@find ./app -name '*.pyc' -exec rm -f {} +
	@find ./app -name '*.pyo' -exec rm -f {} +
	@find ./app -name '__pycache__' -exec rm -fr {} +
	@rm -rf .cache .coverage npm-debug.log tests/__pycache__ tests/*.pyc
	
mysql:
	@docker-compose exec mysql mysql -uroot -proot git_webhook
		
build-db:
	@docker-compose exec app python scripts.py build_db
		
dev:
	@docker-compose -f docker/docker-compose-dev.yml up

celery:
	@celery -A app.celeryInstance worker --loglevel=debug

dev-mysql:
	@mysql -h 127.0.0.1 -uroot -proot git_webhook

test:
	@docker-compose -f docker/docker-compose-test.yml up -d

run:
	@gunicorn -k eventlet -w 1 -b :18340 --log-level=debug run_webhook:app
