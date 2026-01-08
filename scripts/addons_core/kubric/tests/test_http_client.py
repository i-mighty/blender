# SPDX-FileCopyrightText: 2025 Kubric Contributors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""
Tests for Kubric HTTP Client (Blender add-on side)
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import json
import urllib.error


# Mock bpy module for testing
class MockBPY:
    class MockContext:
        class MockPreferences:
            class MockAddon:
                class MockPrefs:
                    agent_server_url = "http://localhost:8000"
                preferences = MockPrefs()
            addons = {"kubric": MockAddon()}
        preferences = MockPreferences()
    context = MockContext()


@pytest.fixture
def mock_bpy(monkeypatch):
    """Mock bpy module"""
    import sys
    sys.modules['bpy'] = MockBPY
    sys.modules['bpy.context'] = MockBPY.context
    sys.modules['bpy.context.preferences'] = MockBPY.context.preferences
    sys.modules['bpy.context.preferences.addons'] = MockBPY.context.preferences.addons
    monkeypatch.setattr('sys.modules', sys.modules)


@pytest.fixture
def http_client(mock_bpy):
    """Create HTTP client instance"""
    from scripts.addons_core.kubric import http_client
    # Reset global client
    http_client._http_client = None
    return http_client.get_client()


def test_http_client_initialization(http_client):
    """Test HTTP client initialization"""
    assert http_client is not None
    assert http_client.base_url == "http://localhost:8000"
    assert http_client.timeout == 30.0


@patch('urllib.request.urlopen')
def test_check_connection_success(mock_urlopen, http_client):
    """Test successful connection check"""
    # Mock successful response
    mock_response = Mock()
    mock_response.status = 200
    mock_response.read.return_value = json.dumps({
        "status": "healthy",
        "version": "0.1.0",
        "mcp_connected": False
    }).encode()
    mock_urlopen.return_value.__enter__.return_value = mock_response
    
    result = http_client.check_connection()
    
    assert result == True
    assert http_client.connected == True


@patch('urllib.request.urlopen')
def test_check_connection_failure(mock_urlopen, http_client):
    """Test failed connection check"""
    # Mock connection error
    mock_urlopen.side_effect = urllib.error.URLError("Connection refused")
    
    result = http_client.check_connection()
    
    assert result == False
    assert http_client.connected == False


@patch('urllib.request.urlopen')
def test_send_message_success(mock_urlopen, http_client):
    """Test successful message sending"""
    # Mock successful response
    mock_response = Mock()
    mock_response.status = 200
    mock_response.read.return_value = json.dumps({
        "response": "Test response",
        "session_id": "test_session",
        "status": "success"
    }).encode()
    mock_urlopen.return_value.__enter__.return_value = mock_response
    
    response = http_client.send_message("Test message")
    
    assert response == "Test response"


@patch('urllib.request.urlopen')
def test_send_message_http_error(mock_urlopen, http_client):
    """Test HTTP error handling"""
    # Mock HTTP error
    mock_urlopen.side_effect = urllib.error.HTTPError(
        url="http://localhost:8000/api/v1/message",
        code=500,
        msg="Internal Server Error",
        hdrs=None,
        fp=None
    )
    
    response = http_client.send_message("Test message")
    
    assert response is None


@patch('urllib.request.urlopen')
def test_send_message_url_error(mock_urlopen, http_client):
    """Test URL error handling"""
    # Mock URL error
    mock_urlopen.side_effect = urllib.error.URLError("Connection refused")
    
    response = http_client.send_message("Test message")
    
    assert response is None
    assert http_client.connected == False


@patch('urllib.request.urlopen')
def test_get_status_success(mock_urlopen, http_client):
    """Test successful status retrieval"""
    # Mock successful response
    mock_response = Mock()
    mock_response.status = 200
    mock_response.read.return_value = json.dumps({
        "agent_initialized": True,
        "mcp_connected": False
    }).encode()
    mock_urlopen.return_value.__enter__.return_value = mock_response
    
    status = http_client.get_status()
    
    assert status["agent_initialized"] == True


def test_send_message_async_callback(http_client):
    """Test async message sending with callback"""
    callback_called = []
    
    def callback(response, error):
        callback_called.append((response, error))
    
    with patch('urllib.request.urlopen') as mock_urlopen:
        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = json.dumps({
            "response": "Async response",
            "status": "success"
        }).encode()
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        http_client.send_message("Test", callback=callback)
        
        # Wait a bit for thread to complete
        import time
        time.sleep(0.1)
        
        assert len(callback_called) == 1
        assert callback_called[0][0] == "Async response"

