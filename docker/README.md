# Docker Deployment

This directory contains Docker configuration files for deploying Kubric Agent in production.

## Quick Start

1. **Copy environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your configuration:**
   ```bash
   # Required: Add your LLM API key
   LLM_API_KEY=your_api_key_here
   ```

3. **Deploy:**
   ```bash
   ./deploy.sh
   ```

   Or manually:
   ```bash
   docker-compose up -d
   ```

## Files

- `Dockerfile.agent` - Kubric Agent container
- `Dockerfile.mcp-server` - Blender MCP Server container (optional)
- `docker-compose.yml` - Orchestration configuration
- `.env.example` - Environment variable template
- `deploy.sh` - Deployment script

## Configuration

Edit `.env` file to configure:
- LLM provider and API key
- Port mappings
- Logging levels
- Network settings

## Management

```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# View logs
docker-compose logs -f kubric-agent

# Restart
docker-compose restart kubric-agent

# Update
./deploy.sh latest
```

## Network Configuration

### Localhost Access (Blender on Host)

The agent needs to access Blender running on your host machine:

**macOS/Windows:**
- Uses `host.docker.internal` (configured automatically)

**Linux:**
- May need to use `--network host` or configure `extra_hosts`

See `DEPLOYMENT.md` for detailed network configuration.

