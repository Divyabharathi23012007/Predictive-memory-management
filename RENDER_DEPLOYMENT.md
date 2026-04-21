# Render Deployment Guide for MemOS

## Quick Deployment Steps

### 1. Set Up Database
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" → "Database" → "MySQL"
3. Name it: `memoria-db`
4. Copy connection details (host, port, user, password)

### 2. Deploy Backend
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: memoria-backend
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Free

4. Add Environment Variables:
   ```
   PYTHONUNBUFFERED=1
   DB_HOST=your-mysql-host.render.com
   DB_PORT=3306
   DB_NAME=memoria_db
   DB_USER=memoria_user
   DB_PASSWORD=memoria_pass
   ```

5. Set Health Check Path: `/`
6. Enable Auto-deploy

### 3. Deploy Frontend
1. Click "New +" → "Static Site"
2. Configure:
   - **Name**: memoria-frontend
   - **Root Directory**: `frontend`
   - **Build Command**: (leave empty)
   - **Publish Directory**: `frontend`

3. Set Routes:
   ```
   /api/* → https://memoria-backend.onrender.com/
   /* → /index.html
   ```

4. Enable Auto-deploy

### 4. Access Your Application
- **Frontend**: https://memoria-frontend.onrender.com
- **Backend API**: https://memoria-backend.onrender.com
- **API Documentation**: https://memoria-backend.onrender.com/docs

## Alternative: Single Service Deployment

For simpler deployment, you can serve both frontend and backend from one service:

1. Create a unified FastAPI app that serves static files
2. Deploy as single Web Service
3. Update frontend to use relative API calls: `/scan` instead of full URLs

## Environment Variables Reference

| Variable | Description | Example |
|-----------|-------------|----------|
| DB_HOST | MySQL host | your-mysql-host.render.com |
| DB_PORT | MySQL port | 3306 |
| DB_NAME | Database name | memoria_db |
| DB_USER | Database user | memoria_user |
| DB_PASSWORD | Database password | memoria_pass |
| PYTHONUNBUFFERED | Python output buffering | 1 |

## Troubleshooting

### Common Issues
- **Database Connection**: Ensure DB_HOST uses correct Render MySQL host
- **CORS Errors**: Verify backend allows frontend origin
- **Build Failures**: Check requirements.txt format
- **Port Issues**: Use $PORT environment variable

### Health Checks
- Backend: `https://memoria-backend.onrender.com/`
- Frontend: `https://memoria-frontend.onrender.com/health`

## Scaling Options

### Free Tier Limits
- 750 hours/month
- 512MB RAM
- Shared CPU
- 10GB outbound transfer

### Paid Plans
- Standard: $7/month (2GB RAM, 2 CPU)
- Pro: $25/month (4GB RAM, 4 CPU)
- Enterprise: Custom pricing

## Custom Domain Setup

1. Go to service settings in Render dashboard
2. Click "Add Custom Domain"
3. Add your domain (e.g., memoria.yourdomain.com)
4. Update DNS records as instructed
5. Enable SSL certificate (automatic)

## Monitoring and Logs

- Access logs via Render dashboard
- Monitor metrics in service overview
- Set up alerts for downtime
- Use Render's built-in monitoring tools

## CI/CD Integration

Render automatically:
- Deploys on GitHub push
- Runs build commands
- Updates services
- Maintains zero-downtime deployments

## Backup Strategy

- Database: Render provides automated backups
- Code: Version control via GitHub
- Configuration: Store in environment variables
- Assets: Use Render's persistent storage
