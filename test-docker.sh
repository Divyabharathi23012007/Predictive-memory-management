#!/bin/bash

echo "🐳 Testing Docker Setup for MemOS..."
echo "=================================="

# Function to check if service is healthy
check_service() {
    local service_name=$1
    local health_url=$2
    local max_attempts=30
    local attempt=1
    
    echo "🔍 Checking $service_name health..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f -s "$health_url" > /dev/null 2>&1; then
            echo "✅ $service_name is healthy!"
            return 0
        fi
        
        echo "⏳ Attempt $attempt/$max_attempts: $service_name not ready yet..."
        sleep 2
        ((attempt++))
    done
    
    echo "❌ $service_name failed to become healthy"
    return 1
}

# Start services
echo "🚀 Starting Docker services..."
docker-compose up -d

# Wait for services to be ready
echo ""
echo "⏱️ Waiting for services to start..."

# Check backend
if check_service "Backend" "http://localhost:8000/"; then
    echo "📊 Backend API Response:"
    curl -s http://localhost:8000/ | head -c 100
    echo ""
fi

# Check frontend
if check_service "Frontend" "http://localhost:3000/health"; then
    echo "🌐 Frontend Health Response:"
    curl -s http://localhost:3000/health
    echo ""
fi

echo ""
echo "🎉 Docker setup test completed!"
echo ""
echo "📱 Access your application:"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
echo ""
echo "🛠️ Useful commands:"
echo "   View logs: docker-compose logs -f"
echo "   Stop:      docker-compose down"
echo "   Restart:   docker-compose restart"
