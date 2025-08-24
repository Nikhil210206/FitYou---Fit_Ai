# 🚀 Deployment Guide

This project supports automatic deployment when pull requests are merged to the main branch.

## Supported Platforms

### 1. Render (Recommended)
- **Auto-deploy**: ✅ Built-in GitHub integration
- **Setup**: Connect GitHub repo at [render.com](https://render.com)
- **Config**: Uses `render.yaml` (already configured)
- **Free tier**: 750 CPU hours/month

### 2. Railway
- **Auto-deploy**: ✅ GitHub integration
- **Setup**: Connect repo at [railway.app](https://railway.app)
- **Free tier**: $5 credit/month
- **GitHub Secret**: Add `RAILWAY_TOKEN` for Actions deployment

### 3. Fly.io
- **Auto-deploy**: ✅ Via GitHub Actions
- **Setup**: Install Fly CLI and create app
- **Free tier**: 3 VMs, 2,160 hours/month
- **GitHub Secret**: Add `FLY_API_TOKEN`

## Environment Variables Required

All platforms need these environment variables:
- `GEMINI_API_KEY` - Your Google Gemini API key
- `PYTHONPATH` - Set to "." (already configured)

## GitHub Actions Workflow

The `.github/workflows/deploy.yml` file handles automatic deployment:
- Triggers on push to main branch
- Triggers when PRs are merged
- Supports multiple deployment targets
- Includes deployment status notifications

## Quick Start

1. **Choose a platform** (Render recommended)
2. **Connect your GitHub repo** to the platform
3. **Add environment variables** in platform dashboard
4. **Add GitHub Secrets** (if using Railway/Fly.io)
5. **Merge a PR** → Automatic deployment! 🎉

## Troubleshooting

- Check GitHub Actions tab for deployment logs
- Verify environment variables are set correctly
- Ensure `requirements.txt` includes all dependencies
- Check platform-specific logs for detailed error messages