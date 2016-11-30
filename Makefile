help:
	@echo "clean|mysql|createdb|dev|dev-mysql|test|run"
	
clean:
	@find ./app -name '*.pyc' -exec rm -f {} +
	@find ./app -name '*.pyo' -exec rm -f {} +
	@find ./app -name '__pycache__' -exec rm -fr {} +
	@rm -rf .cache .coverage npm-debug.log tests/__pycache__ tests/*.pyc
	
mysql:
	@docker-compose exec mysql mysql -uroot -proot git_webhook
		
createdb:
	@docker-compose exec app python manage.py createdb
		
dev:
	@docker-compose -f docker/docker-compose-dev.yml up

dev-mysql:
	@mysql -h 127.0.0.1 -uroot -proot git_webhook

test:
	@docker-compose -f docker/docker-compose-test.yml up -d

run:
	@gunicorn -k eventlet -w 1 -b :18340 --log-level=debug manage:app
