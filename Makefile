.PHONY: help uv-sync uv-run uv-ruff uv-format docker-build docker-run docker-shell

IMAGE ?= synapse
PORT ?= 8000
UPLOADS_VOLUME ?= synapse-uploads

help:
	@echo "Targets:"
	@echo "  uv-sync        Install dependencies with uv"
	@echo "  uv-run         Start the API server with uv"
	@echo "  uv-ruff        Run ruff checks"
	@echo "  uv-format      Run ruff format"
	@echo "  docker-build   Build the Docker image"
	@echo "  docker-run     Run the Docker container"
	@echo "  docker-shell   Open a shell in the Docker image"

uv-sync:
	uv sync

uv-run:
	uv run main.py

uv-ruff:
	uv run ruff check .

uv-format:
	uv run ruff format .

docker-build:
	docker build -t $(IMAGE) .

docker-run:
	docker run --rm -p 127.0.0.1:$(PORT):$(PORT) -p [::1]:$(PORT):$(PORT) -v $(UPLOADS_VOLUME):/app/uploads $(IMAGE)

docker-run-gpu:
	docker run --rm --gpus all -p 127.0.0.1:$(PORT):$(PORT) -p [::1]:$(PORT):$(PORT) -v $(UPLOADS_VOLUME):/app/uploads $(IMAGE)

docker-shell:
	docker run --rm -it --entrypoint /bin/sh $(IMAGE)
