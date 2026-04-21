# Docker Setup for MemOS - Predictive Memory Management

This document explains how to run the MemOS application using Docker containers.

## Prerequisites

- Docker installed on your system
- Docker Compose installed on your system

## Quick Start

1. **Build and start all services:**
   ```bash
   docker-compose up --build
   ```

2. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Backend Health: http://localhost:8000/

## Docker Compose Services

### Backend Service
- **Container Name:** memoria-backend
- **Port:** 8000 (host) → 8000 (container)
- **Health Check:** `/` endpoint every 30 seconds
- **Volumes:** 
  - `./backend:/app` (development)
  - `backend_data:/app/data` (persistent data)

### Frontend Service
- **Container Name:** memoria-frontend
- **Port:** 3000 (host) → 80 (container)
- **Health Check:** `/health` endpoint every 30 seconds
- **Depends on:** Backend service must be healthy

## Development Commands

### Start services in background
```bash
docker-compose up -d
```

### View logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Stop services
```bash
docker-compose down
```

### Rebuild specific service
```bash
docker-compose up --build backend
docker-compose up --build frontend
```

### Access containers
```bash
# Backend container
docker-compose exec backend bash

# Frontend container
docker-compose exec frontend sh
```

## Production Considerations

For production deployment, consider:

1. **Remove development volumes:**
   - Remove the `./backend:/app` volume mount
   - Use only the `backend_data` volume for persistent storage

2. **Add environment variables:**
   ```yaml
   environment:
     - NODE_ENV=production
     - PYTHONPATH=/app
   ```

3. **Add resource limits:**
   ```yaml
   deploy:
     resources:
       limits:
         memory: 512M
         cpus: '0.5'
   ```

4. **Use proper networking:**
   - Configure firewall rules
   - Use HTTPS with SSL certificates

## Troubleshooting

### Common Issues

1. **Port conflicts:**
   - Ensure ports 3000 and 8000 are available
   - Modify ports in `docker-compose.yml` if needed

2. **Permission issues:**
   - Docker might need proper permissions
   - On Linux, add user to docker group: `sudo usermod -aG docker $USER`

3. **Build failures:**
   - Check Docker logs: `docker-compose logs`
   - Ensure all files are properly copied
   - Verify `.dockerignore` files aren't excluding needed files

4. **Health check failures:**
   - Services might need more time to start
   - Check logs for startup errors
   - Verify backend is responding on `/` endpoint

### Debug Commands

```bash
# Check container status
docker-compose ps

# Inspect container
docker-compose inspect backend

# Run health check manually
curl http://localhost:8000/
curl http://localhost:3000/health
```

## Architecture

```
┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │
│   (Nginx)       │    │   (FastAPI)     │
│   Port: 80      │◄──►│   Port: 8000    │
└─────────────────┘    └─────────────────┘
       │                       │
       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐
│   Port: 3000    │    │   Port: 8000    │
│   (Host)        │    │   (Host)        │
└─────────────────┘    └─────────────────┘
```

## Volumes

- `backend_data`: Persistent storage for database and model files
- Mounted volumes are used for development convenience

## Networks

- `memoria-network`: Internal Docker network for service communication
- Services communicate using service names (e.g., `backend:8000`)
