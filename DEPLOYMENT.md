# Kubric Agent Deployment Guide

## Overview

The Kubric Agent can be deployed in several ways depending on the use case. This document covers deployment strategies, with a focus on containerization for production.

## Deployment Architecture

### Components

1. **Kubric Agent** (Backend Service)
   - Runs as a separate process
   - Connects to Blender MCP Server
   - Processes user requests with LLM

2. **Blender MCP Server** (MCP Protocol Server)
   - Connects to Blender MCP Add-on (socket server in Blender)
   - Exposes MCP tools to agents

3. **Blender MCP Add-on** (In Blender)
   - Creates socket server (port 9876)
   - Executes Blender operations

### Deployment Scenarios

#### Scenario 1: Local Development/Testing
- Agent runs on localhost
- Blender runs locally
- All components on same machine

#### Scenario 2: Local Production
- Agent containerized (Docker) on user's machine
- Blender runs locally
- Blender MCP Server runs locally or in container

#### Scenario 3: Remote/Cloud (Advanced)
- Agent in cloud/container
- Blender runs on user's machine
- Network tunneling for Blender MCP connection

## Containerization Strategy

### Why Containerize?

✅ **Benefits:**
- **Dependency isolation**: All Python dependencies bundled
- **Consistency**: Same environment across dev/staging/prod
- **Easy deployment**: Single container to deploy
- **Versioning**: Tag containers with versions
- **Resource limits**: CPU/memory controls
- **Security**: Isolated runtime environment
- **Scaling**: Easy to scale horizontally (if needed)

### Dockerfile Structure

```dockerfile
# Multi-stage build for smaller image
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY kubric_agent/requirements.txt .

# Install Python dependencies
RUN pip install --user --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Copy agent code
COPY kubric_agent/ /app/kubric_agent/

# Non-root user for security
RUN useradd -m -u 1000 agent && \
    chown -R agent:agent /app
USER agent

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Expose port
EXPOSE 8000

# Run agent
CMD ["python", "-m", "kubric_agent.main"]
```

### Docker Compose (Local Development)

```yaml
version: '3.8'

services:
  kubric-agent:
    build:
      context: .
      dockerfile: docker/Dockerfile.agent
    container_name: kubric-agent
    ports:
      - "8000:8000"
    environment:
      - AGENT_HOST=0.0.0.0
      - AGENT_PORT=8000
      - BLENDER_MCP_SERVER_URL=http://host.docker.internal:8001
      - LLM_API_KEY=${LLM_API_KEY}
      - LLM_PROVIDER=anthropic
    volumes:
      # Mount config for persistence
      - ./kubric_agent/config:/app/config:ro
    networks:
      - kubric-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  blender-mcp-server:
    build:
      context: .
      dockerfile: docker/Dockerfile.mcp-server
    container_name: blender-mcp-server
    ports:
      - "8001:8001"
    environment:
      - BLENDER_HOST=host.docker.internal
      - BLENDER_PORT=9876
    networks:
      - kubric-network
    depends_on:
      - kubric-agent
    restart: unless-stopped

networks:
  kubric-network:
    driver: bridge
```

## Production Deployment Options

### Option 1: Local Docker Deployment (Recommended for Most Users)

**Use Case**: Users running Blender locally, want agent running in container

**Setup:**
```bash
# Build image
docker build -t kubric-agent:latest -f docker/Dockerfile.agent .

# Run container
docker run -d \
  --name kubric-agent \
  -p 8000:8000 \
  -e LLM_API_KEY=your_key_here \
  -e BLENDER_MCP_SERVER_URL=http://localhost:8001 \
  --restart unless-stopped \
  kubric-agent:latest
```

**Pros:**
- Easy to manage
- Isolated from system
- Easy updates (just pull new image)

**Cons:**
- Requires Docker installed
- Network configuration needed for localhost access

### Option 2: System Service (systemd/launchd)

**Use Case**: Users who prefer native system services

**Linux (systemd):**
```ini
# /etc/systemd/system/kubric-agent.service
[Unit]
Description=Kubric AI Agent
After=network.target

[Service]
Type=simple
User=kubric
WorkingDirectory=/opt/kubric-agent
Environment="PATH=/opt/kubric-agent/venv/bin"
ExecStart=/opt/kubric-agent/venv/bin/python -m kubric_agent.main
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**macOS (launchd):**
```xml
<!-- ~/Library/LaunchAgents/com.kubric.agent.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.kubric.agent</string>
    <key>ProgramArguments</key>
    <array>
        <string>/opt/kubric-agent/venv/bin/python</string>
        <string>-m</string>
        <string>kubric_agent.main</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>WorkingDirectory</key>
    <string>/opt/kubric-agent</string>
</dict>
</plist>
```

### Option 3: Cloud Deployment (Advanced)

**Use Case**: Remote access, multi-user scenarios

**Considerations:**
- Blender must run on user's machine (can't containerize easily)
- Need secure tunnel for Blender MCP connection
- Network latency considerations
- Authentication/authorization

**Architecture:**
```
User (Blender) → SSH Tunnel → Cloud Agent → LLM API
                → Blender MCP Server (local)
```

## Configuration Management

### Environment Variables

```bash
# Agent Configuration
AGENT_HOST=0.0.0.0
AGENT_PORT=8000

# Blender MCP Server Configuration
BLENDER_MCP_SERVER_URL=http://localhost:8001
BLENDER_MCP_HOST=localhost
BLENDER_MCP_PORT=9876

# LLM Configuration
LLM_PROVIDER=anthropic  # or openai, deepseek, etc.
LLM_API_KEY=your_api_key_here
LLM_MODEL=claude-3-5-sonnet-20241022

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/kubric-agent.log

# Security
API_KEY=optional_api_key_for_kubric_addon
CORS_ORIGINS=http://localhost:8080
```

### Configuration File

```yaml
# kubric_agent/config/production.yaml
agent:
  host: "0.0.0.0"
  port: 8000
  workers: 4
  max_concurrent_requests: 10

blender_mcp:
  server_url: "http://localhost:8001"
  connection_timeout: 30
  retry_attempts: 3

llm:
  provider: "anthropic"
  model: "claude-3-5-sonnet-20241022"
  max_tokens: 4096
  temperature: 0.7

logging:
  level: "INFO"
  file: "/var/log/kubric-agent.log"
  format: "json"

security:
  api_key_required: true
  cors_origins:
    - "http://localhost:*"
    - "http://127.0.0.1:*"
```

## Production Best Practices

### 1. Security

- **API Keys**: Use environment variables or secrets management
- **Network**: Use HTTPS in production
- **Authentication**: Implement API key authentication
- **Rate Limiting**: Prevent abuse
- **Input Validation**: Sanitize all inputs

### 2. Monitoring

- **Health Checks**: `/health` endpoint
- **Metrics**: Prometheus metrics endpoint
- **Logging**: Structured logging (JSON)
- **Error Tracking**: Sentry or similar

### 3. Resource Management

- **CPU/Memory Limits**: Set container limits
- **Connection Pooling**: Reuse connections
- **Request Timeouts**: Prevent hanging requests
- **Circuit Breakers**: Handle upstream failures

### 4. Deployment Pipeline

```bash
# Build
docker build -t kubric-agent:$VERSION -f docker/Dockerfile.agent .
docker tag kubric-agent:$VERSION kubric-agent:latest

# Test
docker run --rm kubric-agent:$VERSION pytest

# Push to registry
docker push kubric-agent:$VERSION
docker push kubric-agent:latest

# Deploy
kubectl set image deployment/kubric-agent agent=kubric-agent:$VERSION
```

## Network Considerations

### Localhost Access

When agent runs in container but needs to access Blender on host:

**Linux:**
```bash
docker run --network host ...
```

**macOS/Windows:**
```bash
docker run --add-host=host.docker.internal:host-gateway ...
# Then use host.docker.internal instead of localhost
```

### Port Mapping

```
Blender MCP Add-on:     localhost:9876  (in Blender)
Blender MCP Server:     localhost:8001  (separate process)
Kubric Agent:           localhost:8000  (container/service)
Kubric Add-on → Agent:  localhost:8000  (from Blender)
```

## Scaling Considerations

### Single User (Current)
- One agent instance per user
- Agent connects to user's local Blender

### Multi-User (Future)
- Agent pool with load balancer
- Each user's Blender connects to different agent
- Authentication/authorization layer
- Session management

## Troubleshooting

### Container Won't Start
- Check logs: `docker logs kubric-agent`
- Verify environment variables
- Check port conflicts
- Verify network connectivity

### Can't Connect to Blender MCP
- Verify Blender MCP add-on is running
- Check firewall rules
- Verify host.docker.internal (macOS/Windows)
- Check port 9876 is accessible

### High Resource Usage
- Set container limits
- Monitor with `docker stats`
- Check for memory leaks
- Optimize LLM calls

## Recommended Deployment

For most users, **Option 1 (Local Docker)** is recommended:

1. **Simple**: Easy to set up and maintain
2. **Isolated**: Doesn't affect system Python
3. **Portable**: Works across platforms
4. **Updatable**: Easy to pull new versions
5. **Containerized**: Can use Docker Compose for full stack

Setup script:
```bash
#!/bin/bash
# deploy.sh

VERSION=${1:-latest}

echo "Deploying Kubric Agent $VERSION..."

# Pull latest image
docker pull kubric-agent:$VERSION

# Stop existing container
docker stop kubric-agent 2>/dev/null || true
docker rm kubric-agent 2>/dev/null || true

# Start new container
docker run -d \
  --name kubric-agent \
  -p 8000:8000 \
  --env-file .env \
  --restart unless-stopped \
  kubric-agent:$VERSION

echo "Kubric Agent deployed!"
docker ps | grep kubric-agent
```

