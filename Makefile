run:
	@echo "Stopping old docker processes"
	docker-compose rm -fs
	
	@echo "Building docker containers"
	docker-compose up --build --remove-orphans -d

stop:
	@echo 'Stopping container...'
	docker-compose stop