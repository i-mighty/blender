# HTTP Communication Implementation

## Overview

Full HTTP communication has been implemented between the Kubric Add-on (Blender) and Kubric Agent (Backend) using FastAPI.

## Architecture

### Components

1. **Kubric Agent HTTP Server** (`kubric_agent/server.py`)
   - FastAPI-based REST API
   - Endpoints: `/health`, `/api/v1/message`, `/api/v1/status`
   - CORS enabled for cross-origin requests
   - Async request handling

2. **Kubric Add-on HTTP Client** (`scripts/addons_core/kubric/http_client.py`)
   - Synchronous HTTP client using `urllib`
   - Background thread support for async operations
   - Connection status checking
   - Error handling

## API Endpoints

### GET /health
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "mcp_connected": false
}
```

### POST /api/v1/message
Process a user message

**Request:**
```json
{
  "message": "Add a cube",
  "session_id": "optional_session_id",
  "user_id": "optional_user_id"
}
```

**Response:**
```json
{
  "response": "I'll create a cube for you...",
  "session_id": "session_id",
  "status": "success"
}
```

### GET /api/v1/status
Get agent status

**Response:**
```json
{
  "agent_initialized": true,
  "mcp_connected": false,
  "mcp_host": "localhost",
  "mcp_port": 8000
}
```

## Communication Flow

```
User types message in Blender
    ↓
Kubric Add-on UI Panel
    ↓
Send Message Operator
    ↓
HTTP Client (http_client.py)
    ↓
HTTP POST to http://localhost:8000/api/v1/message
    ↓
Kubric Agent Server (FastAPI)
    ↓
Kubric Agent (process_message)
    ↓
Response flows back
    ↓
Chat History Updated
    ↓
UI Panel Refreshed
```

## Features Implemented

### ✅ Agent Server
- FastAPI server with async support
- Health check endpoint
- Message processing endpoint
- Status endpoint
- CORS middleware
- Error handling
- Logging

### ✅ Add-on Client
- HTTP client with urllib
- Connection status checking
- Synchronous and asynchronous message sending
- Error handling
- Session management
- Configuration via preferences

### ✅ UI Integration
- Connection status display
- Chat history display
- Input field
- Send button with connection status
- Real-time UI updates

## Usage

### Starting the Agent Server

```bash
# Local Python
cd kubric_agent
pip install -r requirements.txt
python -m kubric_agent.main

# Docker
cd docker
docker-compose up -d kubric-agent
```

### Configuration in Blender

1. Edit > Preferences > Add-ons > Kubric
2. Set "Agent Server URL" (default: `http://localhost:8000`)
3. Save preferences

### Using in Blender

1. Open 3D Viewport
2. Press `N` to open sidebar
3. Click "Kubric" tab
4. Check connection status
5. Type message and click "Send"

## Testing

### Test Agent Server

```bash
# Health check
curl http://localhost:8000/health

# Send message
curl -X POST http://localhost:8000/api/v1/message \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'

# Check status
curl http://localhost:8000/api/v1/status
```

### Test Add-on

1. Enable Kubric add-on in Blender
2. Open Blender console (Window > Toggle System Console)
3. Type message in Kubric panel
4. Check console for HTTP request/response logs

## Error Handling

### Connection Errors
- Connection refused: Agent server not running
- Timeout: Agent server not responding
- Network error: Check firewall/network settings

### Server Errors
- 503: Agent not initialized
- 500: Error processing message
- 400: Invalid request format

All errors are logged and displayed in the UI.

## Next Steps

- [ ] Add authentication (API keys)
- [ ] Add request timeout handling
- [ ] Add retry logic
- [ ] Add WebSocket support for real-time updates
- [ ] Add message queuing for offline support

