# Deployment Guide

This guide covers various ways to deploy X-Gate so it runs 24/7 in the cloud.

## 🚀 One-Click Deploy Options

### Railway (Easiest - Free Tier Available)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

1. Click the button above
2. Sign in with GitHub
3. Set `TELEGRAM_BOT_TOKEN` environment variable
4. Click "Deploy"
5. Done! Your bot is live 🎉

**Free tier:** 500 hours/month (plenty for a bot)

---

### Render (Free Tier Available)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

1. Click the button above
2. Connect your GitHub account
3. Set `TELEGRAM_BOT_TOKEN` in environment variables
4. Click "Apply"
5. Your bot will be running in ~2 minutes

**Free tier:** Always-on free tier available

---

### Fly.io (Free Tier Available)

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Deploy (from project directory)
fly launch
# When prompted for TELEGRAM_BOT_TOKEN, paste your token

# Your bot is now deployed!
fly status
```

**Free tier:** 3 shared-cpu VMs free

---

## 🐳 Docker Deployment

### Any Cloud Provider with Docker Support

Most cloud providers support Docker. Here's how to deploy:

```bash
# Build the image
docker build -t x-gate .

# Run the container
docker run -d \
  --name x-gate \
  -e TELEGRAM_BOT_TOKEN='your_token_here' \
  -v $(pwd)/data:/app/data \
  --restart unless-stopped \
  x-gate
```

#### Recommended Providers:
- **DigitalOcean App Platform** - $5/month, simple Docker deployment
- **Google Cloud Run** - Pay per use, very cheap for bots
- **AWS Lightsail** - $3.50/month for smallest instance
- **Azure Container Instances** - Pay per second

---

## 🖥️ VPS Deployment (For Technical Users)

If you have a VPS (DigitalOcean, Linode, AWS EC2, etc.):

### Option 1: Docker on VPS

```bash
# SSH into your VPS
ssh user@your-vps-ip

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Clone and deploy
git clone https://github.com/randomness11/x-gate.git
cd x-gate

# Create .env file
echo "TELEGRAM_BOT_TOKEN=your_token_here" > .env

# Start with Docker Compose
docker-compose up -d

# Check logs
docker-compose logs -f
```

### Option 2: Direct Python on VPS

```bash
# SSH into your VPS
ssh user@your-vps-ip

# Install Python 3.11+
sudo apt update
sudo apt install python3.11 python3-pip -y

# Clone repository
git clone https://github.com/randomness11/x-gate.git
cd x-gate

# Run setup
./setup.sh
# (Enter your bot token when prompted)

# Run as a service (optional - keeps it running)
# Create systemd service file
sudo nano /etc/systemd/system/x-gate.service
```

**systemd service file:**
```ini
[Unit]
Description=X-Gate Telegram Bot
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/home/yourusername/x-gate
Environment="TELEGRAM_BOT_TOKEN=your_token_here"
ExecStart=/usr/bin/python3 /home/yourusername/x-gate/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Start the service:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable x-gate
sudo systemctl start x-gate

# Check status
sudo systemctl status x-gate

# View logs
sudo journalctl -u x-gate -f
```

---

## 🆓 Free Deployment Options Comparison

| Provider | Free Tier | Setup Time | Difficulty | Best For |
|----------|-----------|------------|------------|----------|
| **Railway** | 500 hrs/mo | 2 min | ⭐ Easy | Beginners |
| **Render** | Always-on | 3 min | ⭐ Easy | Beginners |
| **Fly.io** | 3 VMs | 5 min | ⭐⭐ Medium | Developers |
| **Oracle Cloud** | Generous | 10 min | ⭐⭐⭐ Hard | Advanced users |
| **Google Cloud Run** | 2M requests/mo | 5 min | ⭐⭐ Medium | Pay-per-use |

---

## 📊 Monitoring Your Deployed Bot

After deployment, verify it's working:

1. **Add bot to a test group**
2. **Make it an admin** with delete permissions
3. **Run `/diagnose`** command
4. **Test with a link:** Post `https://x.com/test/123 This is a test message with context`

### Check Logs

**Railway:**
- Go to your project dashboard → Deployments → View Logs

**Render:**
- Dashboard → Your Service → Logs tab

**Fly.io:**
```bash
fly logs
```

**Docker:**
```bash
docker logs x-gate -f
```

**VPS (systemd):**
```bash
sudo journalctl -u x-gate -f
```

---

## 🔧 Troubleshooting Deployment

### Bot doesn't respond

1. **Check logs** for errors
2. **Verify token** is correct in environment variables
3. **Ensure bot is admin** in the group with delete permissions
4. **Check database** volume/disk is mounted correctly

### Database not persisting

Make sure you have a volume/disk mounted:
- **Railway/Render:** Add a persistent disk
- **Docker:** Use `-v` volume mount
- **VPS:** Check file permissions for `data/` directory

### "Permission denied" errors

The bot needs "Delete Messages" permission:
1. Group settings → Administrators
2. Find your bot → Edit
3. Enable "Delete Messages" ✓

---

## 💰 Cost Estimates

**Free Options (Perfect for most users):**
- Railway: Free (500 hrs/mo) - ~$0
- Render: Free tier - ~$0
- Fly.io: Free (3 VMs) - ~$0

**Paid Options (For high-traffic or multiple bots):**
- Railway Hobby: $5/month
- Render Starter: $7/month
- DigitalOcean: $4-6/month
- VPS (Linode/DigitalOcean): $5-12/month

**Recommendation:** Start with Railway or Render free tier. Upgrade only if needed.

---

## 🔄 Updating Your Deployed Bot

### Railway/Render (Auto-deploy from Git)
1. Push changes to your GitHub repo
2. Automatic deployment triggers
3. Done!

### Fly.io
```bash
fly deploy
```

### Docker on VPS
```bash
cd x-gate
git pull
docker-compose down
docker-compose up -d --build
```

### Direct Python on VPS
```bash
cd x-gate
git pull
sudo systemctl restart x-gate
```

---

## 📞 Need Help?

- **Bot not working?** Run `/diagnose` in your group
- **Deployment issues?** Check the logs (see Monitoring section above)
- **Questions?** Open an issue on GitHub

---

**Pro Tip:** For beginners, we strongly recommend Railway or Render. They're the easiest and have generous free tiers perfect for running a Telegram bot 24/7.
