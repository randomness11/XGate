# ⚡ Quick Start - Get Running in 2 Minutes

This is the **fastest** way to get X-Gate running 24/7.

## 🎯 Choose Your Path

### Path 1: Cloud Deploy (Recommended - Runs 24/7 for FREE)

**Best for:** Everyone who wants a bot that just works

1. **Get a bot token:**
   - Open Telegram and message [@BotFather](https://t.me/BotFather)
   - Send `/newbot` and follow instructions
   - Copy the token you receive

2. **Deploy to Railway (Free):**
   - Click: [![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)
   - Sign in with GitHub
   - Paste your bot token in `TELEGRAM_BOT_TOKEN`
   - Click "Deploy"
   - ✅ Done! Your bot is running 24/7

3. **Add to your group:**
   - Add your bot to a Telegram group
   - Make it admin with "Delete Messages" permission
   - Type `/diagnose` to verify it's working

**Total time:** ~2 minutes

---

### Path 2: Run Locally (For Testing)

**Best for:** Testing before deploying, or if you want to run it on your computer

```bash
# 1. Clone and setup
git clone https://github.com/randomness11/x-gate.git
cd x-gate
chmod +x setup.sh
./setup.sh

# 2. Paste your bot token when prompted

# 3. Bot starts automatically!
```

**Then:**
- Add bot to your group
- Make it admin
- Test with `/start` command

**Total time:** ~3 minutes

---

### Path 3: Docker (For Self-Hosting)

**Best for:** If you have a VPS or prefer Docker

```bash
# 1. Clone repo
git clone https://github.com/randomness11/x-gate.git
cd x-gate

# 2. Create .env file
echo "TELEGRAM_BOT_TOKEN=your_token_here" > .env

# 3. Run
docker-compose up -d

# Check logs
docker-compose logs -f
```

**Total time:** ~5 minutes

---

## ✅ Verify It's Working

After setup:

1. **Add bot to a test group**
2. **Make it admin** (tap group name → Administrators → Add bot)
3. **Enable "Delete Messages"** permission
4. **Run `/diagnose`** in the group
5. **Test:** Post `https://x.com/test/123 with some context here`

If the bot responds to `/diagnose`, you're all set! 🎉

---

## 🆘 Troubleshooting

**Bot doesn't respond:**
- Make sure it's an admin with "Delete Messages" permission
- Run `/diagnose` to check configuration

**"Token not configured" error:**
- Check your token is correct (from @BotFather)
- For Railway/Render: Check environment variables
- For local: Check `.env` file exists

**Need more help?**
- Full setup guide: [README.md](README.md)
- Detailed deployment options: [DEPLOYMENT.md](DEPLOYMENT.md)
- Open an issue on GitHub

---

## 🎓 Next Steps

Your bot is now running! You might want to:

- **Customize settings:** Edit `config.yml` or use the setup script
- **Monitor usage:** Use `/stats` command in your group
- **Scale up:** Check [DEPLOYMENT.md](DEPLOYMENT.md) for other hosting options
- **Update rules:** Adjust link limits and context requirements

---

**That's it! Your X-Gate bot is now protecting your Telegram group from link spam.** 🛡️
