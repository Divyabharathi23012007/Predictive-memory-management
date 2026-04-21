# Vercel Deployment Guide for MemOS

## Overview

Vercel is an excellent platform for deploying serverless applications with automatic scaling and global CDN. This guide will help you deploy your MemOS application to Vercel.

## Prerequisites

- Vercel account (free tier available)
- GitHub repository with your code
- Vercel CLI installed (optional)

## Database Setup

### Option 1: Vercel Postgres (Recommended)
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Storage" → "Postgres"
3. Create database named `memoria-db`
4. Copy connection string

### Option 2: External MySQL
1. Use existing MySQL database
2. Configure connection in Vercel environment variables
3. Update database configuration

## Project Structure

```
minipro/
├── vercel.json              # Vercel configuration
├── backend/
│   ├── vercel_app.py       # Serverless entry point
│   ├── app.py             # Original FastAPI app
│   └── requirements.txt
├── frontend/
│   ├── vercel.config.js     # Frontend build config
│   ├── package.json        # Node.js dependencies
│   └── index.html         # Main dashboard
└── README.md
```

## Deployment Steps

### 1. Configure Backend for Serverless

Your `vercel_app.py` is already configured for Vercel serverless deployment:
- Uses `@vercel/python` runtime
- API endpoints prefixed with `/api/`
- Handler set to FastAPI app

### 2. Configure Frontend

The `vercel.config.js` handles:
- Static file serving from `frontend/` directory
- API route rewrites to backend
- Single Page Application routing

### 3. Deploy to Vercel

#### Method A: Git Integration (Recommended)
1. Push your code to GitHub
2. Go to [Vercel Dashboard](https://vercel.com/dashboard)
3. Click "New Project"
4. Import your GitHub repository
5. Vercel will auto-detect configuration

#### Method B: CLI Deployment
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy from project root
vercel --prod
```

### 4. Environment Variables

Configure these in Vercel Dashboard → Settings → Environment Variables:

```bash
# Database Configuration
DB_HOST=your-db-host.vercel.app
DB_PORT=5432
DB_NAME=memoria_db
DB_USER=memoria_user
DB_PASSWORD=your_secure_password

# Application Configuration
PYTHONUNBUFFERED=1
NODE_ENV=production
```

### 5. Database Migration

If using Vercel Postgres:
1. Update `database.py` for PostgreSQL:
```python
# Replace mysql-connector with psycopg2
import psycopg2
from psycopg2.extras import RealDictCursor

# Update connection string
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT", "5432")),
}
```

## Access Your Application

After deployment:
- **Main App**: `https://your-app.vercel.app`
- **API Endpoints**: `https://your-app.vercel.app/api/`
- **API Documentation**: `https://your-app.vercel.app/api/docs`

## Vercel Configuration Files

### vercel.json (Root)
```json
{
  "version": 2,
  "builds": [
    {
      "src": "backend/vercel_app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "backend/vercel_app.py"
    },
    {
      "src": "/(.*)",
      "dest": "frontend/index.html"
    }
  ],
  "env": {
    "PYTHONUNBUFFERED": "1",
    "DB_HOST": "@mysql_host",
    "DB_PORT": "3306",
    "DB_NAME": "memoria_db",
    "DB_USER": "memoria_user",
    "DB_PASSWORD": "@mysql_password"
  }
}
```

### frontend/vercel.config.js
```javascript
const { PHASE_DESTRUCTURE } = require('phaser');

module.exports = {
  experimental: {
    appDir: 'frontend',
  },
  buildCommand: 'npm run build',
  outputDirectory: 'dist',
  installCommand: 'npm install',
  devCommand: 'npm run dev',
  framework: null,
  rewrites: [
    {
      source: '/api/(.*)',
      destination: '/api/$1',
    },
    {
      source: '/(.*)',
      destination: '/index.html',
    },
  ],
};
```

## Vercel Features

### Serverless Functions
- **Auto-scaling**: Handles traffic spikes automatically
- **Global CDN**: Edge deployment worldwide
- **Zero Cold Starts**: Functions stay warm
- **Built-in Monitoring**: Analytics and logs

### Free Tier Limits
- **Bandwidth**: 100GB/month
- **Function Execution**: 10GB-hours/month
- **Duration**: 10 seconds max per function
- **Concurrent Executions**: 1000

### Paid Plans
- **Hobby**: $20/month (100GB bandwidth, 100GB-hrs)
- **Pro**: $100/month (1TB bandwidth, 1000GB-hrs)
- **Enterprise**: Custom pricing

## Troubleshooting

### Common Issues

**Database Connection Errors**
```bash
# Check environment variables
vercel env ls

# Test database connection locally
python -c "
import os
from database import get_connection
os.environ['DB_HOST'] = 'your-host'
print(get_connection())
"
```

**Function Timeouts**
- Optimize database queries
- Use connection pooling
- Implement caching strategies

**Build Failures**
```bash
# Check requirements.txt format
pip install -r requirements.txt

# Test locally
python backend/vercel_app.py
```

### Performance Optimization

**Reduce Cold Starts**
```python
# Keep functions warm with cron jobs
# Use connection pooling
# Minimize imports
```

**Database Optimization**
```sql
-- Add indexes for faster queries
CREATE INDEX idx_memory_timestamp ON memory_samples(timestamp);
CREATE INDEX idx_process_rank ON process_snapshots(rank_position);
```

## Custom Domain Setup

1. Go to Vercel Dashboard → Project → Settings
2. Add custom domain
3. Configure DNS records:
```
A    @     76.76.19.61
CNAME www  cname.vercel-dns.com
```
4. Enable automatic SSL certificate

## Monitoring and Analytics

### Vercel Analytics
- Real-time visitor statistics
- Performance metrics
- Error tracking
- Geographic distribution

### Custom Monitoring
```javascript
// Add to frontend for API monitoring
fetch('/api/scan')
  .then(res => {
    if (!res.ok) {
      console.error('API Error:', res.status);
    }
    return res.json();
  })
  .catch(error => {
    console.error('Network Error:', error);
    // Implement retry logic
  });
```

## CI/CD Integration

### Automatic Deployments
- Connect GitHub repository
- Deploy on push to main branch
- Preview deployments for pull requests
- Rollback capabilities

### GitHub Actions Integration
```yaml
# .github/workflows/deploy.yml
name: Deploy to Vercel
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID }}
          vercel-project-id: ${{ secrets.PROJECT_ID }}
```

## Scaling Strategy

### Horizontal Scaling
- Vercel automatically scales based on demand
- Functions run in multiple regions
- Load balancing handled automatically

### Database Scaling
- Use connection pooling
- Implement read replicas
- Consider managed database services

## Security Best Practices

### Environment Variables
- Use Vercel's encrypted secrets
- Never commit sensitive data
- Rotate database credentials regularly

### API Security
```python
# Add rate limiting
from fastapi import FastAPI, HTTPException
from fastapi.middleware import Middleware

@app.middleware("http")
async def rate_limit_middleware(request, call_next):
    # Implement rate limiting logic
    return await call_next(request)
```

## Backup and Recovery

### Database Backups
- Vercel Postgres: Automatic daily backups
- External MySQL: Configure backup scripts
- Point-in-time recovery available

### Code Backups
- Git version control
- Vercel deployment history
- Environment variable snapshots

This deployment configuration provides a scalable, serverless solution for your MemOS application with Vercel's global infrastructure.
