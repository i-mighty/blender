#!/bin/bash
# Kubric Agent Deployment Script

set -e

VERSION=${1:-latest}
ENV_FILE=${2:-.env}

echo "🚀 Deploying Kubric Agent $VERSION..."

# Check if .env file exists
if [ ! -f "$ENV_FILE" ]; then
    echo "⚠️  Warning: $ENV_FILE not found. Using defaults."
    echo "   Copy .env.example to .env and configure it."
fi

# Build images
echo "📦 Building images..."
docker-compose build

# Pull latest images if version is specified
if [ "$VERSION" != "latest" ]; then
    echo "📥 Pulling image kubric-agent:$VERSION..."
    docker pull kubric-agent:$VERSION || true
fi

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Start new containers
echo "▶️  Starting containers..."
docker-compose up -d

# Wait for health checks
echo "⏳ Waiting for services to be healthy..."
sleep 5

# Check status
echo "✅ Deployment complete!"
echo ""
echo "📊 Container Status:"
docker-compose ps

echo ""
echo "📝 Logs (last 20 lines):"
docker-compose logs --tail=20

echo ""
echo "🔍 To view logs: docker-compose logs -f"
echo "🛑 To stop: docker-compose down"

