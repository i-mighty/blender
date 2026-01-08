# SPDX-FileCopyrightText: 2025 Kubric Contributors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""
Pytest configuration and fixtures for Kubric Agent tests
"""

import pytest
import asyncio
from unittest.mock import Mock, MagicMock
from typing import Generator

from kubric_agent.agent import KubricAgent
from kubric_agent.mcp_client import MCPClient


@pytest.fixture
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_mcp_client():
    """Mock MCP client for testing"""
    client = Mock(spec=MCPClient)
    client.connected = False
    client.host = "localhost"
    client.port = 8000
    client.connect = Mock(return_value=True)
    client.disconnect = Mock()
    client.call_tool = Mock(return_value={"success": True, "result": "test_result"})
    return client


@pytest.fixture
def agent(mock_mcp_client):
    """Create agent instance with mocked MCP client"""
    agent = KubricAgent()
    agent.mcp_client = mock_mcp_client
    return agent


@pytest.fixture
def sample_message_request():
    """Sample message request for testing"""
    return {
        "message": "Add a cube",
        "session_id": "test_session_123",
        "user_id": "test_user"
    }


@pytest.fixture
def sample_message_response():
    """Sample message response for testing"""
    return {
        "response": "I'll create a cube for you.",
        "session_id": "test_session_123",
        "status": "success"
    }

