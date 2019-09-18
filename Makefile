build:
	@echo "----------------------------------------------------------------"
	@echo "Update of djangowebexpe image"
	@echo "----------------------------------------------------------------"
	docker build --no-cache . --tag djangowebexpe
	@echo "----------------------------------------------------------------"
	@echo "Image is now build you can run instance using 'make run'
	@echo "----------------------------------------------------------------"

run: 
	@echo "----------------------------------------------------------------"
	@echo "Process to run new instance"
	@echo "----------------------------------------------------------------"
	docker run -p 8000:8000 -it -d --name webexpeinstance djangowebexpe
	@echo "----------------------------------------------------------------"
	@echo "Your docker instance is now launched with name 'webexpeinstance'"
	@echo "Your website is now accessible at http://localhost:8000"
	@echo "----------------------------------------------------------------"

stop:
	@echo "----------------------------------------------------------------"
	@echo "Process to stop current instance"
	@echo "----------------------------------------------------------------"
	docker stop webexpeinstance
	@echo "----------------------------------------------------------------"
	@echo "App is now stopped"
	@echo "----------------------------------------------------------------"

remove:
	@echo "----------------------------------------------------------------"
	@echo "Process to stop current instance"
	@echo "----------------------------------------------------------------"
	docker stop webexpeinstance
	docker rm webexpeinstance
	@echo "----------------------------------------------------------------"
	@echo "App is now stopped and removed"
	@echo "----------------------------------------------------------------"

deploy: build run
