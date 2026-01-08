# SPDX-FileCopyrightText: 2025 Kubric Contributors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""
Integration tests for end-to-end communication
"""

import pytest
import requests
import time
import subprocess
import signal
import os
from fastapi.testclient import TestClient
from kubric_agent.server import app


@pytest.fixture(scope="module")
def agent_server():
    """Start agent server for integration tests"""
    import uvicorn
    import threading
    
    def run_server():
        uvicorn.run(app, host="127.0.0.1", port=8001, log_level="error")
    
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Wait for server to start
    max_attempts = 10
    for _ in range(max_attempts):
        try:
            response = requests.get("http://127.0.0.1:8001/health", timeout=1)
            if response.status_code == 200:
                break
        except:
            time.sleep(0.5)
    else:
        pytest.skip("Could not start test server")
    
    yield "http://127.0.0.1:8001"
    
    # Server will stop when thread dies (daemon=True)


@pytest.mark.integration
def test_agent_server_health(agent_server):
    """Test agent server health endpoint via HTTP"""
    response = requests.get(f"{agent_server}/health", timeout=5)
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


@pytest.mark.integration
def test_agent_server_message_endpoint(agent_server):
    """Test message endpoint via HTTP"""
    response = requests.post(
        f"{agent_server}/api/v1/message",
        json={"message": "Hello from integration test"},
        timeout=10
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert data["status"] == "success"


@pytest.mark.integration
def test_agent_server_status_endpoint(agent_server):
    """Test status endpoint via HTTP"""
    response = requests.get(f"{agent_server}/api/v1/status", timeout=5)
    
    assert response.status_code == 200
    data = response.json()
    assert "agent_initialized" in data


@pytest.mark.integration
def test_agent_server_concurrent_requests(agent_server):
    """Test server handles concurrent requests"""
    import concurrent.futures
    
    def send_request():
        response = requests.post(
            f"{agent_server}/api/v1/message",
            json={"message": "Concurrent test"},
            timeout=10
        )
        return response.status_code == 200
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(send_request) for _ in range(5)]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]
    
    assert all(results), "All concurrent requests should succeed"


@pytest.mark.integration
def test_agent_server_error_handling(agent_server):
    """Test server error handling"""
    # Invalid JSON
    response = requests.post(
        f"{agent_server}/api/v1/message",
        data="invalid json",
        headers={"Content-Type": "application/json"},
        timeout=5
    )
    
    assert response.status_code == 422  # Validation error

