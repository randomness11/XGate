<div align="center">

```text
██╗  ██╗       ██████╗  █████╗ ████████╗███████╗
╚██╗██╔╝      ██╔════╝ ██╔══██╗╚══██╔══╝██╔════╝
 ╚███╔╝ █████╗██║  ███╗███████║   ██║   █████╗  
 ██╔██╗ ╚════╝██║   ██║██╔══██║   ██║   ██╔══╝  
██╔╝ ██╗      ╚██████╔╝██║  ██║   ██║   ███████╗
╚═╝  ╚═╝       ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝
```

</div>

# X-Gate
### The Ultimate Telegram Guardian for X Links

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

---

**X-Gate** is a powerful, high-performance Telegram bot designed to keep your groups clean and spam-free. It enforces strict moderation on X (formerly Twitter) links, ensuring that every shared link adds value to the conversation.

## ⚡ TL;DR - Get Started in 60 Seconds

**Want the fastest setup?** → **[QUICKSTART.md](QUICKSTART.md)** ← Click here!

**Or run this:**

```bash
git clone https://github.com/yourusername/x-gate.git
cd x-gate
chmod +x setup.sh && ./setup.sh
```

**That's it!** Just paste your bot token when prompted, and you're done. The bot handles everything else automatically.

> 💡 **Pro Tip:** For 24/7 operation, use our free cloud deployment instead of running locally. See [☁️ Deploy to Cloud](#️-deploy-to-cloud-run-247-for-free) below.

---

## ☁️ Deploy to Cloud (Run 24/7 for Free!)

The setup above runs locally. To keep your bot running 24/7, deploy to the cloud:

### One-Click Deploy (Easiest)

**Railway (Recommended for beginners):**

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

Just click, add your bot token, and deploy. **Free tier included!**

**Other Options:**
- **Render** - Free tier, auto-deploys from GitHub
- **Fly.io** - 3 free VMs
- **Google Cloud Run** - Pay per use (very cheap for bots)

📖 **[Full Deployment Guide →](DEPLOYMENT.md)** (Railway, Render, Fly.io, VPS, Docker, etc.)

---

## 🛡️ Key Features

- **智能 Smart Regex**: Accurately detects X/Twitter links, ignoring trailing punctuation.
- **⚡ Rate Limiting**: Limit the number of links a user can post per week to prevent flooding.
- **📝 Context Enforcement**: Require users to add text/commentary with their links (no more naked link spam!).
- **🌍 Timezone Aware**: Built with UTC consistency for reliable usage tracking across the globe.
- **🐋 Docker Ready**: Deploy in seconds with the included Docker configuration.

## 🚀 Quick Start

### Super Easy Setup (Recommended)

**Get started in under 2 minutes!**

1. **Clone and run the setup script**
   ```bash
   git clone https://github.com/yourusername/x-gate.git
   cd x-gate
   chmod +x setup.sh
   ./setup.sh
   ```

2. **That's it!** The interactive setup will:
   - Ask for your bot token (get one from [@BotFather](https://t.me/BotFather))
   - Save it securely to `.env` file
   - Let you customize settings (or use smart defaults)
   - Install dependencies automatically
   - Start your bot

### Alternative: Environment Variable Setup

If you prefer environment variables:

```bash
# 1. Set your bot token
export TELEGRAM_BOT_TOKEN='your_token_here'

# 2. Install and run
pip install -r requirements.txt
python bot.py
```

**No config file needed!** The bot works with just the token.

### Docker Setup (Local or Self-Hosted)

```bash
# Create .env file
echo "TELEGRAM_BOT_TOKEN=your_token_here" > .env

# Run with Docker Compose (easiest)
docker-compose up -d

# Or run with Docker directly
docker run -d \
  --name x-gate \
  -e TELEGRAM_BOT_TOKEN='your_token' \
  -v $(pwd)/data:/app/data \
  --restart unless-stopped \
  telegram-x-moderator

# Check logs
docker-compose logs -f
# or
docker logs x-gate -f
```

> **Note:** For 24/7 cloud deployment, see the [☁️ Deploy to Cloud](#️-deploy-to-cloud-run-247-for-free) section above.

## 📱 Adding Bot to Your Group

1. **Add the bot to your Telegram group**
2. **Make it an admin** with "Delete Messages" permission
3. **Type `/diagnose`** in the group to verify setup
4. **Done!** The bot will automatically:
   - Send a welcome message with instructions
   - Start moderating X links based on your rules

### Helpful Commands

- `/start` - View bot rules and settings
- `/stats` - Check your X link usage this week
- `/diagnose` - Troubleshoot bot configuration

## ⚙️ Configuration (Optional)

The bot works great with default settings, but you can customize it:

**Option 1: Interactive setup**
```bash
./setup.sh  # Answer prompts to customize
```

**Option 2: Create/edit config.yml**
```yaml
rules:
  max_links_per_week: 3     # Links allowed per user per week
  count_per_link: true      # Count every link individually
  require_context: true     # Require text with links
  min_context_length: 30    # Minimum context characters
```

**Default Settings:**
- Max 3 X links per user per week
- Context required (30+ characters)
- Counts each link individually
- Auto-cleanup of old data (30 days)

## 🚢 Deployment Quick Reference

| Method | Best For | Cost | Setup Time | Command |
|--------|----------|------|------------|---------|
| 🚂 **Railway** | Beginners | Free* | 2 min | Click deploy button |
| 🎨 **Render** | Auto-deploy | Free* | 3 min | Click deploy button |
| ✈️ **Fly.io** | Developers | Free* | 5 min | `fly launch` |
| 🐳 **Docker** | Self-hosting | VPS cost | 5 min | `docker-compose up -d` |
| 🖥️ **VPS** | Full control | $5/mo | 10 min | `./setup.sh` |

*Free tiers available - see [DEPLOYMENT.md](DEPLOYMENT.md) for details

**Recommended:** Railway or Render for hassle-free 24/7 operation.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- Inspired by the need for cleaner, more meaningful group discussions

---
<div align="center">
  <sub>Built with ❤️ by <a href="https://x.com/ankitkr0">Ankit</a></sub>
  <br>
  <sub>⭐ Star this repo if you find it useful!</sub>
</div>

