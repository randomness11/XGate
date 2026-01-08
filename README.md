<div align="center">

<div align="center">

```text
██╗  ██╗       ██████╗  █████╗ ████████╗███████╗
╚██╗██╔╝      ██╔════╝ ██╔══██╗╚══██╔══╝██╔════╝
 ╚███╔╝ █████╗██║  ███╗███████║   ██║   █████╗  
 ██╔██╗ ╚════╝██║   ██║██╔══██║   ██║   ██╔══╝  
██╔╝ ██╗      ╚██████╔╝██║  ██║   ██║   ███████╗
╚═╝  ╚═╝       ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝
```

# X-Gate
### The Ultimate Telegram Guardian for X Links

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

</div>

---

**X-Gate** is a powerful, high-performance Telegram bot designed to keep your groups clean and spam-free. It enforces strict moderation on X (formerly Twitter) links, ensuring that every shared link adds value to the conversation.

## 🛡️ Key Features

- **智能 Smart Regex**: Accurately detects X/Twitter links, ignoring trailing punctuation.
- **⚡ Rate Limiting**: Limit the number of links a user can post per week to prevent flooding.
- **📝 Context Enforcement**: Require users to add text/commentary with their links (no more naked link spam!).
- **🌍 Timezone Aware**: Built with UTC consistency for reliable usage tracking across the globe.
- **🐋 Docker Ready**: Deploy in seconds with the included Docker configuration.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- A Telegram Bot Token (from [@BotFather](https://t.me/BotFather))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/x-gate.git
   cd x-gate
   ```

2. **Configure usage**
   ```bash
   cp config.example.yml config.yml
   # Edit config.yml and add your bot_token
   ```

3. **Run**
   ```bash
   # Using Python
   pip install -r requirements.txt
   python bot.py

   # Using Docker
   docker-compose up -d
   ```

## ⚙️ Configuration

Customize `config.yml` to fit your community's needs:

```yaml
rules:
  max_links_per_week: 3     # Strict limit
  count_per_link: true      # Count every link in a message
  require_context: true     # Enforce commentary
  min_context_length: 30    # Minimum characters of context
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---
<div align="center">
  <sub>Built with ❤️ by <a href="https://x.com/ankitkr0">Ankit</a></sub>
</div>

