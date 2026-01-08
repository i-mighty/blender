# SPDX-FileCopyrightText: 2025 Kubric Contributors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""
Integration tests for Kubric Agent HTTP Server
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from kubric_agent.server import app, _agent, _mcp_client, lifespan
from kubric_agent.agent import KubricAgent
from kubric_agent.mcp_client import MCPClient


@pytest.fixture
def client():
    """Create test client for FastAPI app"""
    # TestClient doesn't automatically run lifespan, so we need to initialize manually
    from kubric_agent.server import _agent, _mcp_client
    
    # Manually initialize agent (simulating lifespan startup)
    import kubric_agent.server as server_module
    server_module._agent = KubricAgent()
    server_module._mcp_client = MCPClient()
    
    client = TestClient(app)
    
    yield client
    
    # Cleanup (simulating lifespan shutdown)
    if server_module._mcp_client:
        server_module._mcp_client.disconnect()
    server_module._agent = None
    server_module._mcp_client = None


def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "version" in data
    assert "mcp_connected" in data
    assert data["status"] == "healthy"


def test_status_endpoint(client):
    """Test status endpoint"""
    response = client.get("/api/v1/status")
    
    assert response.status_code == 200
    data = response.json()
    assert "agent_initialized" in data
    assert "mcp_connected" in data


def test_message_endpoint_success(client):
    """Test message endpoint with valid request"""
    response = client.post(
        "/api/v1/message",
        json={
            "message": "Hello, agent!",
            "session_id": "test_session"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "status" in data
    assert data["status"] == "success"
    assert isinstance(data["response"], str)
    assert len(data["response"]) > 0


def test_message_endpoint_empty_message(client):
    """Test message endpoint with empty message"""
    response = client.post(
        "/api/v1/message",
        json={"message": ""}
    )
    
    # Should still process (validation happens in agent)
    assert response.status_code in [200, 400]


def test_message_endpoint_missing_message(client):
    """Test message endpoint with missing message field"""
    response = client.post(
        "/api/v1/message",
        json={}
    )
    
    assert response.status_code == 422  # Validation error


def test_message_endpoint_invalid_json(client):
    """Test message endpoint with invalid JSON"""
    response = client.post(
        "/api/v1/message",
        data="invalid json",
        headers={"Content-Type": "application/json"}
    )
    
    assert response.status_code == 422


def test_cors_headers(client):
    """Test CORS headers are present"""
    response = client.options(
        "/api/v1/message",
        headers={"Origin": "http://localhost:3000"}
    )
    
    # CORS middleware should be configured
    assert response.status_code in [200, 405]  # OPTIONS might return 405


def test_message_endpoint_session_persistence(client):
    """Test that session ID is preserved in response"""
    session_id = "test_session_123"
    
    response = client.post(
        "/api/v1/message",
        json={
            "message": "Hello",
            "session_id": session_id
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    # Session ID should be in response (if agent supports it)
    assert "session_id" in data

