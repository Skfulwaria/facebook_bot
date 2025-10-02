# Facebook Comment Bot 🤖

Complete automated commenting system for Facebook with GitHub hosting support.

## 🚀 Features

- ✅ **GitHub Hosted** - Run from anywhere
- ✅ **Auto Token Filter** - Remove invalid tokens automatically  
- ✅ **100 Token Limit** - Maximum safety limit
- ✅ **Continuous Run** - Until manually stopped
- ✅ **Multi-Platform** - Termux, Heroku, Replit, VPS
- ✅ **Page Token Support** - Optional page integration
- ✅ **Safety Delays** - Configurable timing between comments

## 📱 Quick Start

### Termux Installation:
```bash
# Method 1: Auto installer
python install.py

# Method 2: Manual setup
pkg update && pkg upgrade
pkg install python git wget -y
pip install requests colorama
wget https://raw.githubusercontent.com/BrokenNadeem/fb-bot/main/fb_bot.py
python fb_bot.py
