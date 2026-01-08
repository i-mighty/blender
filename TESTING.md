# Kubric Testing Strategy

## Overview

This document outlines the testing strategy for Kubric, covering both the agent backend and the Blender add-on, including connectivity testing.

## Test Structure

```
kubric_agent/tests/
├── __init__.py
├── conftest.py              # Pytest fixtures
├── test_agent.py            # Agent unit tests
├── test_server.py           # HTTP server tests
├── test_mcp_client.py       # MCP client tests
└── test_integration.py      # End-to-end integration tests

scripts/addons_core/kubric/tests/
├── __init__.py
└── test_http_client.py      # Add-on HTTP client tests
```

## Test Categories

### 1. Unit Tests

**Purpose**: Test individual components in isolation

**Coverage**:
- Agent message processing
- Agent context management
- MCP client operations
- HTTP client operations

**Run**: `pytest kubric_agent/tests/test_agent.py -v`

### 2. Integration Tests

**Purpose**: Test component interactions

**Coverage**:
- HTTP server endpoints
- Request/response handling
- Error handling
- Concurrent request handling

**Run**: `pytest kubric_agent/tests/test_server.py -v`

### 3. End-to-End Tests

**Purpose**: Test full system integration

**Coverage**:
- Agent server startup/shutdown
- HTTP communication
- Multiple concurrent requests
- Error scenarios

**Run**: `pytest kubric_agent/tests/test_integration.py -v -m integration`

### 4. Connectivity Tests

**Purpose**: Test communication between add-on and agent

**Coverage**:
- Connection establishment
- Message sending/receiving
- Error handling
- Reconnection logic

**Run**: `pytest scripts/addons_core/kubric/tests/test_http_client.py -v`

## Running Tests

### Prerequisites

```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-mock requests
```

### Run All Tests

```bash
# From project root
pytest kubric_agent/tests/ -v
pytest scripts/addons_core/kubric/tests/ -v
```

### Run Specific Test Categories

```bash
# Unit tests only
pytest kubric_agent/tests/test_agent.py -v

# Integration tests only
pytest kubric_agent/tests/test_integration.py -v -m integration

# HTTP server tests
pytest kubric_agent/tests/test_server.py -v

# Add-on client tests
pytest scripts/addons_core/kubric/tests/test_http_client.py -v
```

### Run with Coverage

```bash
pip install pytest-cov
pytest kubric_agent/tests/ --cov=kubric_agent --cov-report=html
```

## Manual Testing Guide

### 1. Test Agent Server Locally

```bash
# Start agent server
cd kubric_agent
python -m kubric_agent.main

# In another terminal, test endpoints
curl http://localhost:8000/health
curl -X POST http://localhost:8000/api/v1/message \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

### 2. Test Add-on Connectivity

**In Blender**:
1. Enable Kubric add-on
2. Open 3D Viewport (N for sidebar)
3. Click "Kubric" tab
4. Check connection status (should show "Agent: Connected" if server running)
5. Type message and click "Send"
6. Check Blender console for HTTP logs

**Expected Behavior**:
- Connection status updates correctly
- Messages send successfully
- Responses appear in chat history
- Errors display user-friendly messages

### 3. Test End-to-End Flow

**Setup**:
1. Start agent server: `python -m kubric_agent.main`
2. Start Blender MCP add-on (in Blender)
3. Enable Kubric add-on (in Blender)

**Test Flow**:
1. Open Kubric panel in Blender
2. Verify all status indicators show "Connected"
3. Send message: "Hello"
4. Verify response appears in chat history
5. Send message: "Add a cube" (once LLM is integrated)
6. Verify cube is created in Blender

## Test Scenarios

### Happy Path

1. ✅ Agent server starts successfully
2. ✅ Add-on connects to agent
3. ✅ Message sent and received
4. ✅ Response displayed in UI
5. ✅ Chat history updated

### Error Scenarios

1. ✅ Agent server not running → Connection error displayed
2. ✅ Invalid server URL → Error message shown
3. ✅ Network timeout → Graceful error handling
4. ✅ Invalid JSON response → Error handling
5. ✅ Server returns 500 → Error message displayed

### Edge Cases

1. ✅ Empty message → Warning displayed
2. ✅ Very long message → Handled correctly
3. ✅ Special characters → Properly escaped
4. ✅ Concurrent messages → Handled correctly
5. ✅ Server restart → Reconnection works

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: pip install -r kubric_agent/requirements.txt
      - run: pip install pytest pytest-asyncio pytest-mock pytest-cov
      - run: pytest kubric_agent/tests/ --cov=kubric_agent
```

## Test Data

### Sample Messages

```python
SAMPLE_MESSAGES = [
    "Hello",
    "Add a cube",
    "Create a sphere at origin",
    "Make the cube red",
    "Delete the selected object",
    "Show me the scene information",
]
```

### Mock Responses

```python
MOCK_RESPONSES = {
    "greeting": "Hello! I'm the Kubric AI agent.",
    "create_cube": "I'll create a cube for you.",
    "error": "I encountered an error processing your request.",
}
```

## Debugging Tests

### Verbose Output

```bash
pytest -v -s  # Verbose with print statements
pytest --pdb   # Drop into debugger on failure
```

### Test Specific Function

```bash
pytest kubric_agent/tests/test_agent.py::test_process_message_basic -v
```

### Run Tests in Parallel

```bash
pip install pytest-xdist
pytest -n auto  # Auto-detect CPU count
```

## Coverage Goals

- **Unit Tests**: 80%+ coverage
- **Integration Tests**: Critical paths covered
- **E2E Tests**: Main user flows covered

## Next Steps

1. ✅ Basic test structure created
2. 🚧 Add LLM integration tests (when implemented)
3. 🚧 Add MCP tool call tests (when implemented)
4. 🚧 Add Blender add-on UI tests
5. 🚧 Add performance/load tests

## Troubleshooting

### Tests Fail to Import Modules

```bash
# Make sure you're in the right directory
cd /path/to/blender-git/blender
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest kubric_agent/tests/
```

### Blender Add-on Tests Need bpy

Use mocking (see `test_http_client.py` for example) or run tests in Blender's Python environment.

### Integration Tests Can't Start Server

- Check port 8001 is available
- Verify uvicorn is installed
- Check firewall settings

