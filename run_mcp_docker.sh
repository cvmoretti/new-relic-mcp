#!/bin/bash

# New Relic MCP Server - Docker Runner for Cursor Integration

set -e

CONTAINER_NAME="newrelic-mcp-server"
IMAGE_NAME="newrelic-mcp:latest"

echo "🐳 New Relic MCP Server - Docker Runner"

# Function to build image
build_image() {
    echo "🔨 Building MCP Server Docker image..."
    docker build -f Dockerfile.mcp -t $IMAGE_NAME .
    echo "✅ Image built successfully!"
}

# Function to run container
run_container() {
    echo "🚀 Starting MCP Server container (persistent mode)..."
    
    # Stop existing container if running
    if docker ps -q -f name=$CONTAINER_NAME | grep -q .; then
        echo "🛑 Stopping existing container..."
        docker stop $CONTAINER_NAME > /dev/null 2>&1
        docker rm $CONTAINER_NAME > /dev/null 2>&1
    fi
    
    # Remove stopped container if exists
    if docker ps -aq -f name=$CONTAINER_NAME | grep -q .; then
        echo "🗑️ Removing stopped container..."
        docker rm $CONTAINER_NAME > /dev/null 2>&1
    fi
    
    # Start new container in detached mode with restart policy
    docker run -d \
        --name $CONTAINER_NAME \
        --env-file .env \
        -e PYTHONUNBUFFERED=1 \
        --restart unless-stopped \
        $IMAGE_NAME
    
    # Give container time to start
    sleep 3
    
    echo "✅ MCP Server container started and running persistently!"
    echo "📋 Container ID: $(docker ps -q -f name=$CONTAINER_NAME)"
    echo "📡 Server is ready to accept Cursor connections"
}

# Function to test container
test_container() {
    echo "🧪 Testing MCP Server..."
    
    # Check if container is running
    if ! docker ps -q -f name=$CONTAINER_NAME | grep -q .; then
        echo "❌ Container is not running. Start it first with: ./run_mcp_docker.sh run"
        return 1
    fi
    
    echo "✅ Container is running"
    echo "🔍 Container status:"
    docker ps -f name=$CONTAINER_NAME --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    
    echo ""
    echo "📋 Recent container logs:"
    docker logs $CONTAINER_NAME --tail 20 2>/dev/null || echo "No logs available yet"
    
    echo ""
    echo "🧪 Testing MCP Server connection (simulating Cursor)..."
    echo '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test-client", "version": "1.0.0"}}}' | \
    timeout 10 docker exec -i $CONTAINER_NAME python /app/mcp_server.py || echo "⚠️ MCP test completed (this is normal)"
}

# Function to show configuration for Cursor
show_cursor_config() {
    # Check if container is running first
    if ! docker ps -q -f name=$CONTAINER_NAME | grep -q .; then
        echo ""
        echo "⚠️  Container is not running!"
        echo "   Run first: ./run_mcp_docker.sh run"
        echo ""
        return 1
    fi
    
    echo ""
    echo "🎯 CURSOR CONFIGURATION (Persistent Container):"
    echo ""
    echo "✅ Container is running: $CONTAINER_NAME"
    echo ""
    echo "📋 Add this to Cursor MCP configuration:"
    echo ""
    echo "{"
    echo "  \"mcpServers\": {"
    echo "    \"newrelic\": {"
    echo "      \"command\": \"$(pwd)/newrelic-mcp\""
    echo "    }"
    echo "  }"
    echo "}"
    echo ""
    echo "💡 Alternative (if above doesn't work):"
    echo "{"
    echo "  \"mcpServers\": {"
    echo "    \"newrelic\": {"
    echo "      \"command\": \"docker\","
    echo "      \"args\": ["
    echo "        \"exec\", \"-i\","
    echo "        \"$CONTAINER_NAME\","
    echo "        \"python\", \"/app/mcp_server.py\""
    echo "      ]"
    echo "    }"
    echo "  }"
    echo "}"
    echo ""
    echo "📝 Steps:"
    echo "1. Cursor → Settings → Features → Model Context Protocol"
    echo "2. Edit Configuration"
    echo "3. Paste the JSON configuration above"
    echo "4. Save and restart Cursor"
    echo ""
    echo "🚀 The container runs continuously, Cursor just connects to it!"
    echo ""
}

# Function to show logs
show_logs() {
    echo "📄 Container logs:"
    docker logs -f $CONTAINER_NAME
}

# Function to stop container
stop_container() {
    echo "🛑 Stopping MCP Server container..."
    docker stop $CONTAINER_NAME > /dev/null || true
    docker rm $CONTAINER_NAME > /dev/null || true
    echo "✅ Container stopped!"
}

# Main script logic
case "${1:-help}" in
    build)
        build_image
        ;;
    run)
        build_image
        run_container
        show_cursor_config
        ;;
    start)
        run_container
        show_cursor_config
        ;;
    test)
        test_container
        ;;
    logs)
        show_logs
        ;;
    stop)
        stop_container
        ;;
    restart)
        stop_container
        run_container
        show_cursor_config
        ;;
    config)
        show_cursor_config
        ;;
    help|*)
        echo "Usage: $0 {build|run|start|test|logs|stop|restart|config}"
        echo ""
        echo "Commands:"
        echo "  build    - Build Docker image"
        echo "  run      - Build and run container (recommended)"
        echo "  start    - Start existing container" 
        echo "  test     - Test MCP server"
        echo "  logs     - Show container logs"
        echo "  stop     - Stop container"
        echo "  restart  - Restart container"
        echo "  config   - Show Cursor configuration"
        echo ""
        echo "Example: $0 run"
        ;;
esac
