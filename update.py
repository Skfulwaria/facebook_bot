import os
import requests

print("🔄 Updating Facebook Bot...")

# Backup current files
os.system('cp tokens.txt tokens_backup.txt')
os.system('cp comments.txt comments_backup.txt')

# Remove old files
os.system('rm -rf facebook_bot')

# Clone latest version
os.system('git clone https://github.com/Skfulwaria/facebook_bot.git')

# Restore backups
os.system('cp tokens_backup.txt facebook_bot/tokens.txt')
os.system('cp comments_backup.txt facebook_bot/comments.txt')

print("✅ Update complete!")
print("🚀 Run: cd facebook_bot && python facebook_bot.py")
