
.PHONY: treatment-service-run
treatment-service-run:
	- docker network create treatment_network
	- mkdir -p /src/docker/treatment-service/
	docker build -t treatment_db_image -f db.Dockerfile .
	docker build -t treatment_frontend_image -f frontend.Dockerfile .
	docker build -t treatment_consumer_image -f consumer.Dockerfile .
	docker build -t treatment_backend_image -f backend.Dockerfile .
	docker-compose -f docker-compose.yaml up -d

.PHONY: docker-cleanup
docker-cleanup:
	docker ps -aq | xargs sudo docker rm -f && docker system prune -a && docker volume prune

.PHONY: backend-run
backend-run:
	docker build -t treatment_backend_image -f backend.Dockerfile .
	docker-compose -f docker-compose.yaml up -d backend