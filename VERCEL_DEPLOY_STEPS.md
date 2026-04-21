# Vercel Deployment Steps for MemOS

## Step 1: Database Setup

### Option A: Vercel Postgres (Recommended)
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Storage" → "Postgres"
3. Create database named `memoria-db`
4. Copy the connection string

### Option B: External MySQL
1. Use your existing MySQL database
2. Get connection details (host, port, user, password, database name)

## Step 2: Configure Environment Variables

In your Vercel project dashboard, add these Environment Variables:

```bash
# Database Configuration
DB_HOST=your_database_host
DB_PORT=5432  # 3306 for MySQL, 5432 for PostgreSQL
DB_NAME=memoria_db
DB_USER=your_username
DB_PASSWORD=your_password

# Application Configuration
PYTHONUNBUFFERED=1
```

## Step 3: Update Database Configuration

### For Vercel Postgres (PostgreSQL)
Update `backend/database.py` to use PostgreSQL:

```python
# Replace mysql-connector with psycopg2
import psycopg2
from psycopg2.extras import RealDictCursor

# Update connection configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT", "5432")),
}

def get_connection():
    """Establish PostgreSQL database connection"""
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        return connection
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None
```

### For MySQL (Keep current setup)
Your current `database.py` should work with MySQL.

## Step 4: Update Requirements

Update `backend/requirements.txt`:

```txt
fastapi
uvicorn
psutil
numpy
scikit-learn
mysql-connector-python  # Keep for MySQL
# psycopg2-binary  # Add for PostgreSQL
```

## Step 5: Deploy to Vercel

### Method 1: Automatic Deployment (Recommended)
1. Push all changes to GitHub
2. Vercel will automatically redeploy
3. Check deployment logs for errors

### Method 2: Manual Redeploy
1. Go to Vercel Dashboard
2. Click your project
3. Click "Deployments"
4. Click "Redeploy"

## Step 6: Test Your Application

After deployment, test these URLs:
- **Frontend**: `https://your-app-name.vercel.app`
- **API Root**: `https://your-app-name.vercel.app/`
- **API Scan**: `https://your-app-name.vercel.app/api/scan`
- **API Docs**: `https://your-app-name.vercel.app/docs`

## Common Issues and Solutions

### Database Connection Error
**Problem**: `Error connecting to database`
**Solution**: 
1. Check environment variables in Vercel dashboard
2. Verify database is accessible from Vercel
3. Update connection string format

### Function Timeout
**Problem**: Functions timeout after 10 seconds
**Solution**:
1. Optimize database queries
2. Add connection pooling
3. Reduce processing time

### CORS Error
**Problem**: Frontend can't access API
**Solution**: 
1. Check CORS middleware in backend
2. Update API calls in frontend
3. Verify route configuration

### Build Error
**Problem**: Build fails during deployment
**Solution**:
1. Check `requirements.txt` format
2. Verify all imports are correct
3. Check for syntax errors

## Quick Deployment Checklist

- [ ] Database created and accessible
- [ ] Environment variables configured
- [ ] `vercel.json` properly set up
- [ ] `requirements.txt` includes all dependencies
- [ ] Frontend API calls updated
- [ ] Code pushed to GitHub
- [ ] Deployment successful
- [ ] All endpoints tested

## Post-Deployment Monitoring

### Check Vercel Dashboard
1. Go to "Functions" tab
2. Check function logs
3. Monitor performance metrics
4. Set up alerts for errors

### Test Key Features
1. Memory scanning works
2. Process data displays
3. Historical data loads
4. ML predictions generate
5. Dashboard updates correctly

## Scaling Considerations

### Free Tier Limits
- 100GB bandwidth/month
- 10GB function execution hours
- 10-second function timeout
- 1000 concurrent executions

### When to Upgrade
- High traffic volume
- Longer processing times needed
- More concurrent users
- Advanced monitoring required

This guide should help you successfully deploy MemOS to Vercel!
