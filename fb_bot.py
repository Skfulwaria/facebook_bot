  import requests
import random
import time
from datetime import datetime
import os
import sys

# Colors for Termux
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'

def clear_screen():
    os.system('clear')

def show_banner():
    print(f"""{Colors.CYAN}
╔══════════════════════════════════════════════════════════════════════════════╗
║                   FACEBOOK BOT - SKFULWARIA EDITION                         ║
║                   GitHub: https://github.com/Skfulwaria/facebook_bot        ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Colors.RESET}""")

class FacebookBot:
    def __init__(self):
        self.tokens = []
        self.comments = []
    
    def load_tokens(self):
        """Load tokens from tokens.txt file"""
        try:
            with open('tokens.txt', 'r') as f:
                self.tokens = [line.strip() for line in f if line.strip()]
            print(f"{Colors.GREEN}✅ Loaded {len(self.tokens)} tokens{Colors.RESET}")
            return True
        except:
            print(f"{Colors.RED}❌ Error loading tokens.txt{Colors.RESET}")
            return False
    
    def load_comments(self):
        """Load comments from comments.txt file"""
        try:
            with open('comments.txt', 'r', encoding='utf-8') as f:
                self.comments = [line.strip() for line in f if line.strip()]
            print(f"{Colors.GREEN}✅ Loaded {len(self.comments)} comments{Colors.RESET}")
            return True
        except:
            print(f"{Colors.RED}❌ Error loading comments.txt{Colors.RESET}")
            return False
    
    def check_token(self, token):
        """Check if token is valid"""
        try:
            url = f'https://graph.facebook.com/v17.0/me?access_token={token}'
            response = requests.get(url, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def get_user_info(self, token):
        """Get user information from token"""
        try:
            url = f'https://graph.facebook.com/v17.0/me?fields=name,id&access_token={token}'
            response = requests.get(url, timeout=10)
            data = response.json()
            return data.get('name', 'Unknown'), data.get('id', 'Unknown')
        except:
            return "Unknown", "Unknown"
    
    def post_comment(self, token, post_id, comment):
        """Post comment to Facebook"""
        try:
            url = f"https://graph.facebook.com/v17.0/{post_id}/comments"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36',
                'Authorization': f'Bearer {token}'
            }
            data = {
                'message': comment,
                'access_token': token
            }
            
            response = requests.post(url, headers=headers, data=data, timeout=30)
            return response.status_code == 200
        except:
            return False
    
    def run(self):
        clear_screen()
        show_banner()
        
        print(f"{Colors.YELLOW}🕒 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.RESET}")
        print(f"{Colors.GREEN}{'='*70}{Colors.RESET}")
        
        # Load tokens and comments
        if not self.load_tokens():
            return
        
        if not self.load_comments():
            return
        
        # Filter valid tokens
        print(f"{Colors.YELLOW}🔍 Checking token validity...{Colors.RESET}")
        valid_tokens = []
        for token in self.tokens:
            if self.check_token(token):
                valid_tokens.append(token)
                print(f"{Colors.GREEN}✅ Valid token: {token[:20]}...{Colors.RESET}")
            else:
                print(f"{Colors.RED}❌ Invalid token: {token[:20]}...{Colors.RESET}")
        
        if not valid_tokens:
            print(f"{Colors.RED}❌ No valid tokens found!{Colors.RESET}")
            return
        
        print(f"{Colors.GREEN}🎯 {len(valid_tokens)} valid tokens ready{Colors.RESET}")
        
        # Get post ID
        post_id = input(f"\n{Colors.GREEN}📝 Enter Post ID: {Colors.RESET}").strip()
        if not post_id:
            print(f"{Colors.RED}❌ Post ID required!{Colors.RESET}")
            return
        
        # Get delay settings
        try:
            delay = int(input(f"{Colors.GREEN}⏰ Delay between comments (seconds): {Colors.RESET}") or "120")
        except:
            delay = 120
        
        print(f"{Colors.GREEN}{'='*70}{Colors.RESET}")
        print(f"{Colors.CYAN}🚀 Starting bot...{Colors.RESET}")
        print(f"{Colors.YELLOW}📍 Press Ctrl+C to stop{Colors.RESET}")
        
        success = 0
        failed = 0
        token_index = 0
        
        try:
            while True:
                current_token = valid_tokens[token_index % len(valid_tokens)]
                token_index += 1
                
                # Check token before use
                if not self.check_token(current_token):
                    print(f"{Colors.RED}🗑️ Token expired, skipping...{Colors.RESET}")
                    continue
                
                user_name, user_id = self.get_user_info(current_token)
                comment = random.choice(self.comments)
                
                print(f"\n{Colors.CYAN}👤 User: {user_name}{Colors.RESET}")
                print(f"{Colors.WHITE}   📝 Post: {post_id}{Colors.RESET}")
                print(f"{Colors.WHITE}   💬 Comment: {comment[:50]}...{Colors.RESET}")
                
                if self.post_comment(current_token, post_id, comment):
                    print(f"{Colors.GREEN}   ✅ Comment posted!{Colors.RESET}")
                    success += 1
                else:
                    print(f"{Colors.RED}   ❌ Failed to post{Colors.RESET}")
                    failed += 1
                
                print(f"{Colors.BLUE}   📊 Stats: ✅{success} | ❌{failed}{Colors.RESET}")
                print(f"{Colors.YELLOW}   ⏳ Waiting {delay} seconds...{Colors.RESET}")
                
                time.sleep(delay)
                
        except KeyboardInterrupt:
            print(f"\n\n{Colors.RED}🛑 Bot stopped by user{Colors.RESET}")
        
        print(f"\n{Colors.GREEN}{'='*70}{Colors.RESET}")
        print(f"{Colors.CYAN}📊 Final Report:{Colors.RESET}")
        print(f"{Colors.GREEN}   ✅ Successful: {success}{Colors.RESET}")
        print(f"{Colors.RED}   ❌ Failed: {failed}{Colors.RESET}")
        print(f"{Colors.YELLOW}   🕒 Ended: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.RESET}")

if __name__ == "__main__":
    bot = FacebookBot()
    bot.run()
