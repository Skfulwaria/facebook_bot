  import os
import requests

print("📱 Installing Facebook Bot - Skfulwaria Edition")

# Update packages
os.system('pkg update -y && pkg upgrade -y')

# Install Python and Git
os.system('pkg install python -y')
os.system('pkg install git -y')

# Install Python dependencies
os.system('pip install requests colorama')

# Clone repository
os.system('git clone https://github.com/Skfulwaria/facebook_bot.git')

print("✅ Installation complete!")
print("📁 Folder: facebook_bot")
print("🚀 Run: cd facebook_bot && python facebook_bot.py")
