# SPDX-FileCopyrightText: 2025 Kubric Contributors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""
Unit tests for Kubric Agent
"""

import pytest
from kubric_agent.agent import KubricAgent


@pytest.mark.asyncio
async def test_agent_initialization():
    """Test agent initialization"""
    agent = KubricAgent()
    assert agent is not None
    assert agent.conversation_history == []
    assert agent.mcp_client is not None


@pytest.mark.asyncio
async def test_process_message_basic(agent):
    """Test basic message processing"""
    response = await agent.process_message("Hello")
    
    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 0


@pytest.mark.asyncio
async def test_process_message_conversation_history(agent):
    """Test that messages are stored in conversation history"""
    await agent.process_message("Hello")
    await agent.process_message("How are you?")
    
    assert len(agent.conversation_history) == 4  # 2 user + 2 assistant messages
    assert agent.conversation_history[0]["role"] == "user"
    assert agent.conversation_history[0]["content"] == "Hello"
    assert agent.conversation_history[1]["role"] == "assistant"


@pytest.mark.asyncio
async def test_process_message_with_session(agent):
    """Test message processing with session ID"""
    response = await agent.process_message("Test message", session_id="test_session")
    
    assert response is not None
    # Session ID should be stored in context
    context = agent.get_context()
    assert "session" in context


@pytest.mark.asyncio
async def test_get_context(agent):
    """Test context retrieval"""
    await agent.process_message("Test message")
    
    context = agent.get_context()
    assert "history" in context
    assert "mcp_connected" in context
    assert len(context["history"]) > 0


@pytest.mark.asyncio
async def test_agent_response_keywords(agent):
    """Test agent responses to different keywords"""
    # Test greeting
    response = await agent.process_message("Hello")
    assert "Hello" in response or "ready" in response.lower()
    
    # Test cube creation request
    response = await agent.process_message("create a cube")
    assert "cube" in response.lower() or "create" in response.lower()


@pytest.mark.asyncio
async def test_agent_error_handling(agent):
    """Test error handling in message processing"""
    # Should not raise exception even with empty message
    response = await agent.process_message("")
    assert response is not None

