import os
import requests
import sys

def print_banner():
    banner = """
\033[1;36m
╔══════════════════════════════════════════════════════════════════════════════╗
║                   FACEBOOK COMMENT BOT - TERMUX INSTALLER                   ║
║                         GitHub Hosted Version                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
\033[0m
    """
    print(banner)

def setup_termux():
    print("\033[1;33m🔧 Setting up Termux environment...\033[0m")
    
    os.system('pkg update -y && pkg upgrade -y')
    
    packages = ['python', 'git', 'wget']
    for pkg in packages:
        os.system(f'pkg install {pkg} -y')
    
    print("\033[1;33m📦 Installing Python dependencies...\033[0m")
    os.system('pip install requests colorama')
    
    print("\033[1;32m✅ Termux setup completed!\033[0m")

def download_bot():
    print("\033[1;33m📥 Downloading Facebook Comment Bot...\033[0m")
    
    files = {
        'fb_bot.py': 'https://raw.githubusercontent.com/BrokenNadeem/fb-bot/main/fb_bot.py',
        'tokens.txt': 'https://raw.githubusercontent.com/BrokenNadeem/fb-bot/main/tokens.txt',
        'comments.txt': 'https://raw.githubusercontent.com/BrokenNadeem/fb-bot/main/comments.txt'
    }
    
    for filename, url in files.items():
        try:
            response = requests.get(url)
            if response.status_code == 200:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(response.text)
                print(f"\033[1;32m✅ Downloaded {filename}\033[0m")
            else:
                print(f"\033[1;31m❌ Failed to download {filename}\033[0m")
        except Exception as e:
            print(f"\033[1;31m❌ Error downloading {filename}: {e}\033[0m")
    
    return True

def main():
    print_banner()
    
    print("\033[1;34m🚀 Starting installation...\033[0m")
    
    setup_termux()
    
    if download_bot():
        print("\n\033[1;32m🎉 Installation Complete!\033[0m")
        print("\033[1;36m📖 Usage Instructions:\033[0m")
        print("  1. Edit tokens.txt - Add your Facebook tokens")
        print("  2. Edit comments.txt - Add your comments")
        print("  3. Run: python fb_bot.py")
        print("\n\033[1;33m🔑 Default Password: Broken123\033[0m")
        print("\033[1;33m⚠️  Use responsibly and respect Facebook's ToS\033[0m")
    else:
        print("\033[1;31m❌ Installation failed!\033[0m")

if __name__ == "__main__":
    main()
