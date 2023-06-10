build:
	docker build -t mip-sample . --no-cache

run:
	docker run -p 8000:8000 -v $(shell pwd):/app -it mip-sample

curl:
	curl -X POST http://localhost:8000/run -H 'Content-Type: application/json'
