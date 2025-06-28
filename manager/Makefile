.PHONY: up down

up:
	docker build -t ghcr.io/platform-engineering-org/afula:latest .
	kind create cluster
	kind load docker-image ghcr.io/platform-engineering-org/afula:latest
	kubectl apply -f deploy/postgres-secret.yaml
	kubectl apply -f deploy/postgres.yaml
	kubectl apply -f deploy/afula.yaml
	sleep 20
	kubectl port-forward service/afula 5000:5000 &

down:
	kind delete cluster
