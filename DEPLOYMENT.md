# Deployment Guide - Precision Farming Application on Render

This guide provides comprehensive instructions for deploying the AgriSmart - AI-Powered Agricultural Management System to Render's free tier.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Deployment Steps](#deployment-steps)
3. [Environment Variables Configuration](#environment-variables-configuration)
4. [Database Configuration](#database-configuration)
5. [Accessing Your Application](#accessing-your-application)
6. [Troubleshooting](#troubleshooting)
7. [Monitoring and Logs](#monitoring-and-logs)
8. [Post-Deployment Checklist](#post-deployment-checklist)

## Prerequisites

Before deploying to Render, ensure you have:

1. **GitHub Account**: Your code must be in a GitHub repository
2. **Render Account**: Sign up at [https://render.com](https://render.com)
   - Free tier is sufficient for this application
3. **Repository Access**: Ensure your repository is public or you've granted Render access to private repositories

## Deployment Steps

### Method 1: Using Render Blueprint (Recommended)

The repository includes a `render.yaml` file that automates the deployment process.

1. **Sign in to Render**
   - Go to [https://dashboard.render.com](https://dashboard.render.com)
   - Sign in with your GitHub account or create a new Render account

2. **Create New Blueprint**
   - Click "New +" button in the top navigation
   - Select "Blueprint"
   - Connect your GitHub account if not already connected
   - Select the repository: `tejaslakshmangith/precisionfarming`
   - Render will automatically detect the `render.yaml` file

3. **Configure Blueprint**
   - Review the service configuration from `render.yaml`
   - Click "Apply" to create the service
   - Render will automatically start the deployment

4. **Wait for Deployment**
   - Initial deployment may take 5-10 minutes
   - Monitor the deployment logs in the Render dashboard

### Method 2: Manual Web Service Creation

If you prefer manual setup or need to customize settings:

1. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the `precisionfarming` repository

2. **Configure Service Settings**
   ```
   Name: precisionfarming (or your preferred name)
   Region: Oregon (or closest to your users)
   Branch: main
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app
   Plan: Free
   ```

3. **Advanced Settings**
   - Auto-Deploy: Yes (automatically deploy on git push)
   - Health Check Path: `/` (optional)

## Environment Variables Configuration

Render requires certain environment variables to be set for production deployment.

### Required Environment Variables

1. **Navigate to Environment Tab**
   - In your service dashboard, click "Environment"
   - Click "Add Environment Variable"

2. **Add the following variables:**

   | Key | Value | Notes |
   |-----|-------|-------|
   | `FLASK_ENV` | `production` | Sets Flask to production mode |
   | `SECRET_KEY` | (generate secure key) | Used for session security |
   | `PYTHON_VERSION` | `3.11.0` | Python version for deployment |

3. **Generate SECRET_KEY**
   
   Option A - Let Render generate:
   - When adding `SECRET_KEY`, click "Generate Value"
   - Render will create a secure random string
   
   Option B - Generate manually:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
   - Copy the output and use as `SECRET_KEY` value

### Optional Environment Variables

These can be configured based on your needs:

```bash
FLASK_DEBUG=False
LOG_LEVEL=INFO
```

## Database Configuration

The application uses SQLite by default, which is suitable for the free tier.

### SQLite (Default - Recommended for Free Tier)

- No additional configuration needed
- Database file: `agriculture.db`
- Automatically created on first run
- **Important**: SQLite data will be lost on service restarts/redeploys
- For persistent data, consider upgrading to a managed database

### Data Persistence Notes

⚠️ **Important**: Render's free tier uses ephemeral storage:
- Database and ML model files are recreated on each deployment
- User data will be lost when the service restarts
- For production with persistent data, consider:
  - Upgrading to a paid Render plan with persistent disks
  - Using Render's PostgreSQL database service
  - Using an external database service

### Machine Learning Models

The application includes ML models that are trained/loaded on startup:
- Models are stored in the `instance/` directory
- On first run, models will be trained from the dataset
- Training happens automatically during initialization
- Subsequent runs will load pre-trained models if available

## Accessing Your Application

### After Deployment

1. **Get Your URL**
   - Once deployed, Render provides a URL like: `https://precisionfarming-xxxx.onrender.com`
   - Find it in the service dashboard, top of the page

2. **First Visit**
   - Navigate to your application URL
   - You should see the AgriSmart landing page
   - Initial load may take 30-60 seconds (free tier cold start)

3. **Test the Application**
   - Create a new user account via the "Register" page
   - Login with your credentials
   - Test the features:
     - Crop Prediction
     - Fertilizer Recommendation
     - Irrigation Scheduling

### Free Tier Limitations

Be aware of Render's free tier characteristics:
- **Cold Starts**: Service spins down after 15 minutes of inactivity
- **First Request**: May take 30-60 seconds after inactivity
- **RAM**: 512 MB
- **Bandwidth**: 100 GB/month
- **Build Minutes**: 500 minutes/month

## Troubleshooting

### Common Issues and Solutions

#### 1. Build Failures

**Problem**: Build fails with dependency errors

**Solution**:
```bash
# Check requirements.txt has all dependencies
# Common missing dependencies:
pip install -r requirements.txt
```

**Verify Python version**:
- Ensure `PYTHON_VERSION` environment variable matches your local development version

#### 2. Application Won't Start

**Problem**: Service shows "Starting" but never becomes "Live"

**Solutions**:
- Check logs for errors (see Monitoring section)
- Verify `gunicorn` is installed: Check `requirements.txt` includes `gunicorn>=21.2.0`
- Ensure start command is: `gunicorn app:app`
- Check that `app.py` exports the Flask app as `app`

#### 3. 502 Bad Gateway

**Problem**: Accessing the URL shows "502 Bad Gateway"

**Solutions**:
- Service might be starting (wait 30-60 seconds)
- Check application logs for startup errors
- Verify the application binds to `0.0.0.0` not `127.0.0.1`

**Fix** (if needed in app.py):
```python
# Change from:
app.run(host='127.0.0.1', port=5000)
# To:
app.run(host='0.0.0.0', port=5000)
```

#### 4. Missing ML Models or Data

**Problem**: Application errors about missing model files

**Solution**:
- Ensure the `Data/` directory with `Crop_recommendation.csv` is in the repository
- Models will be auto-trained on first startup if not present
- Check logs to see model training progress

#### 5. Database Errors

**Problem**: Database-related errors on startup

**Solutions**:
- Ensure SQLite database is configured in `config.py`
- Database is auto-created on first run
- Check `instance/` directory is in `.gitignore` (ephemeral storage)

#### 6. Import Errors

**Problem**: `ModuleNotFoundError` in logs

**Solutions**:
- Verify all dependencies are in `requirements.txt`
- Check for typos in import statements
- Ensure package versions are compatible

### Debugging Steps

1. **Check Service Logs** (see Monitoring section)
2. **Verify Environment Variables** are set correctly
3. **Review Build Logs** for dependency installation issues
4. **Test Locally** with `gunicorn app:app` before deploying
5. **Check Repository** - ensure all necessary files are committed

## Monitoring and Logs

### Accessing Logs

1. **Navigate to Logs Tab**
   - In your service dashboard, click "Logs"
   - Shows real-time application output

2. **Types of Logs**
   - **Deploy Logs**: Shows build and deployment process
   - **Service Logs**: Shows application runtime logs
   - **Event Logs**: Shows service events (restarts, deploys)

3. **Reading Logs**
   - Look for `INFO` messages for normal operation
   - `WARNING` messages indicate potential issues
   - `ERROR` messages indicate failures
   - Application startup shows initialization messages

### Example Log Messages

**Successful Startup**:
```
Starting gunicorn 21.2.0
Listening at: http://0.0.0.0:10000
Using worker: sync
Booting worker with pid: 123
```

**ML Model Loading**:
```
Loading crop prediction model...
Model loaded successfully
```

**Database Initialization**:
```
Creating database tables...
Database initialized
```

### Monitoring Service Health

1. **Service Metrics**
   - Click "Metrics" tab to see:
     - CPU usage
     - Memory usage
     - Request count
     - Response times

2. **Set Up Alerts** (Optional)
   - Configure email notifications for service issues
   - Available in Render dashboard settings

### Performance Monitoring

Monitor these metrics for optimal performance:
- **Response Time**: Should be under 1 second for most requests
- **Memory Usage**: Should stay under 400 MB (free tier limit: 512 MB)
- **CPU Usage**: Spikes are normal during ML predictions

## Post-Deployment Checklist

After successful deployment, verify:

- [ ] Service is "Live" in Render dashboard
- [ ] Application URL is accessible
- [ ] Landing page loads correctly
- [ ] User registration works
- [ ] User login works
- [ ] Dashboard displays after login
- [ ] Crop prediction feature works
- [ ] Fertilizer recommendation feature works
- [ ] Irrigation scheduling feature works
- [ ] No errors in service logs
- [ ] Environment variables are set correctly
- [ ] Auto-deploy is enabled (optional)

## Updating Your Application

### Automatic Deployment (Recommended)

With auto-deploy enabled:
1. Push changes to your `main` branch on GitHub
2. Render automatically detects the push
3. Triggers a new build and deployment
4. Monitor progress in the "Events" tab

### Manual Deployment

If auto-deploy is disabled:
1. Navigate to your service dashboard
2. Click "Manual Deploy" button
3. Select "Clear build cache & deploy" if needed
4. Monitor deployment logs

## Additional Resources

- **Render Documentation**: [https://render.com/docs](https://render.com/docs)
- **Render Status**: [https://status.render.com](https://status.render.com)
- **Community Support**: [https://community.render.com](https://community.render.com)
- **Render Blog**: [https://render.com/blog](https://render.com/blog)

## Getting Help

If you encounter issues:

1. **Check this guide** for common solutions
2. **Review service logs** for error messages
3. **Render Community Forum**: Post questions at community.render.com
4. **GitHub Issues**: Report bugs in the repository
5. **Render Support**: Contact support@render.com for account issues

## Security Best Practices

1. **Never commit `.env` file** to version control
2. **Use strong `SECRET_KEY`** - generate a new one for production
3. **Keep dependencies updated** - regularly update `requirements.txt`
4. **Review logs regularly** for suspicious activity
5. **Enable HTTPS** (Render provides this automatically)

## Cost Considerations

**Free Tier Includes**:
- 750 hours/month of runtime
- 100 GB bandwidth/month
- 500 build minutes/month
- Automatic SSL certificates
- Custom domains (optional)

**When to Upgrade**:
- Need persistent storage for database
- Require faster cold starts
- Need more RAM (>512 MB)
- Higher traffic volume

---

**Last Updated**: January 2026  
**Application Version**: 1.0  
**Render Platform**: Free Tier

For application-specific documentation, see:
- [README.md](README.md) - Project overview
- [INSTALLATION.md](INSTALLATION.md) - Local installation guide
- [USER_GUIDE.md](USER_GUIDE.md) - Application usage guide
