# Kubric Makefile for testing and development

.PHONY: test test-unit test-integration test-all test-coverage test-connectivity install-dev clean

# Test targets
test:
	pytest kubric_agent/tests/ -v

test-unit:
	pytest kubric_agent/tests/test_agent.py kubric_agent/tests/test_mcp_client.py -v

test-integration:
	pytest kubric_agent/tests/test_integration.py -v -m integration

test-server:
	pytest kubric_agent/tests/test_server.py -v

test-all:
	pytest kubric_agent/tests/ scripts/addons_core/kubric/tests/ -v

test-coverage:
	pytest kubric_agent/tests/ --cov=kubric_agent --cov-report=html --cov-report=term

test-connectivity:
	./test_connectivity.sh

# Development
install-dev:
	pip install -r kubric_agent/requirements.txt
	pip install pytest pytest-asyncio pytest-mock pytest-cov pytest-xdist

# Clean
clean:
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".coverage" -exec rm -r {} +
	find . -type d -name "htmlcov" -exec rm -r {} +

# Run agent server
run-agent:
	cd kubric_agent && python -m kubric_agent.main

# Docker
docker-build:
	docker build -t kubric-agent:latest -f docker/Dockerfile.agent .

docker-test:
	docker run --rm kubric-agent:latest pytest kubric_agent/tests/ -v

