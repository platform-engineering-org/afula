.PHONY: build up down clean

build:
	docker build -t ghcr.io/platform-engineering-org/afula-manager:latest -f manager/Dockerfile .
	docker build -t ghcr.io/platform-engineering-org/afula-processor:latest -f processor/Dockerfile .

up: build
	kind create cluster
	kind load docker-image ghcr.io/platform-engineering-org/afula-manager:latest
	kind load docker-image ghcr.io/platform-engineering-org/afula-processor:latest
	kubectl apply -f manager/deploy/postgres-secret.yaml
	kubectl apply -f manager/deploy/postgres.yaml
	kubectl apply -f manager/deploy/manager.yaml
	export $(cat processor/deploy/.env | xargs)
	envsubst < processor/deploy/secrets.yaml | kubectl apply -f -
	kubectl apply -f processor/deploy/processor.yaml
	sleep 20
	kubectl port-forward service/manager 5000:5000 &

down:
	kind delete cluster

clean:
	docker system prune --all --force
