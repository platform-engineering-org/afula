.PHONY: up down

up:
	docker build -t ghcr.io/platform-engineering-org/afula-manager:latest manager
	docker build -t ghcr.io/platform-engineering-org/processor:latest processor
	kind create cluster
	kind load docker-image ghcr.io/platform-engineering-org/afula-manager:latest
	kind load docker-image ghcr.io/platform-engineering-org/processor:latest
	kubectl apply -f manager/deploy/postgres-secret.yaml
	kubectl apply -f manager/deploy/postgres.yaml
	kubectl apply -f manager/deploy/manager.yaml
	kubectl apply -f processor/deploy/secrets.yaml
	kubectl apply -f processor/deploy/processor.yaml
	sleep 20
	kubectl port-forward service/manager 5000:5000 &

down:
	kind delete cluster
