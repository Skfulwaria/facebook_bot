import requests
import random
import time
import json
from datetime import datetime
import os
import sys

# Color codes for Termux
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def clear_screen():
    os.system('clear')

def show_banner():
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════════════════════╗
║                   FACEBOOK COMMENT BOT - GITHUB HOSTED                      ║
║                         Complete Auto System                               ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Colors.RESET}
{Colors.GREEN}✅ GitHub Hosted | ✅ Auto Token Filter | ✅ Multi-Platform
{Colors.YELLOW}📱 Run on: Termux, Heroku, Replit, VPS, Local PC
{Colors.BLUE}🔧 Features: 100 Token Limit, Auto Remove Expired, Continuous Run
{Colors.RESET}
{Colors.MAGENTA}👑 Developer: Broken Nadeem | Version: 3.0
{Colors.RESET}
"""
    print(banner)

class FacebookCommentBot:
    def __init__(self):
        self.valid_tokens = []
        self.config = {
            'max_tokens': 100,
            'min_delay': 120,
            'max_delay': 300
        }
    
    def check_password(self):
        """Simple password protection"""
        print(f"{Colors.YELLOW}🔒 Password Protection{Colors.RESET}")
        print(f"{Colors.GREEN}{'═'*60}{Colors.RESET}")
        
        local_pass = "Broken123"
        password = input(f"{Colors.GREEN}Enter Password: {Colors.RESET}")
        
        if password != local_pass:
            print(f"{Colors.RED}❌ Incorrect Password!{Colors.RESET}")
            sys.exit()
        
        print(f"{Colors.GREEN}✅ Password Verified{Colors.RESET}")
        print(f"{Colors.GREEN}{'═'*60}{Colors.RESET}")

    def load_tokens(self, source_type):
        """Load tokens from different sources"""
        tokens = []
        
        if source_type == "1":
            # Local file
            file_path = input(f"{Colors.GREEN}📁 Enter tokens file path: {Colors.RESET}").strip()
            if not file_path:
                file_path = "tokens.txt"
            
            try:
                with open(file_path, 'r') as f:
                    tokens = [line.strip() for line in f if line.strip()]
                print(f"{Colors.GREEN}✅ Loaded {len(tokens)} tokens from {file_path}{Colors.RESET}")
            except:
                print(f"{Colors.RED}❌ Cannot read tokens file{Colors.RESET}")
        
        elif source_type == "2":
            # GitHub URL
            github_url = input(f"{Colors.GREEN}🔗 Enter GitHub raw URL: {Colors.RESET}").strip()
            try:
                response = requests.get(github_url, timeout=15)
                if response.status_code == 200:
                    tokens = [line.strip() for line in response.text.split('\n') if line.strip()]
                    print(f"{Colors.GREEN}✅ Loaded {len(tokens)} tokens from GitHub{Colors.RESET}")
                else:
                    print(f"{Colors.RED}❌ Failed to load from GitHub{Colors.RESET}")
            except Exception as e:
                print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}")
        
        elif source_type == "3":
            # Direct input
            token_input = input(f"{Colors.GREEN}📝 Enter tokens (comma separated): {Colors.RESET}").strip()
            tokens = [t.strip() for t in token_input.split(',') if t.strip()]
            print(f"{Colors.GREEN}✅ Loaded {len(tokens)} tokens{Colors.RESET}")
        
        # Apply 100 token limit
        if len(tokens) > self.config['max_tokens']:
            print(f"{Colors.YELLOW}⚠️  Limited to first {self.config['max_tokens']} tokens{Colors.RESET}")
            tokens = tokens[:self.config['max_tokens']]
        
        return tokens

    def validate_tokens(self, tokens):
        """Validate and filter tokens"""
        print(f"{Colors.YELLOW}🔍 Validating {len(tokens)} tokens...{Colors.RESET}")
        print(f"{Colors.GREEN}{'─'*60}{Colors.RESET}")
        
        valid_tokens = []
        
        for i, token in enumerate(tokens, 1):
            token_display = token[:20] + "..." if len(token) > 20 else token
            print(f"{Colors.WHITE}   Checking {i}/{len(tokens)}: {token_display}{Colors.RESET}", end='\r')
            
            if self.is_token_valid(token):
                valid_tokens.append(token)
                print(f"{Colors.GREEN}   ✅ Token {i}: Valid{Colors.RESET}")
            else:
                print(f"{Colors.RED}   ❌ Token {i}: Invalid - Removed{Colors.RESET}")
            
            time.sleep(0.5)
        
        print(f"\n{Colors.GREEN}✅ Valid tokens: {len(valid_tokens)}{Colors.RESET}")
        print(f"{Colors.RED}❌ Invalid tokens: {len(tokens) - len(valid_tokens)}{Colors.RESET}")
        
        if not valid_tokens:
            print(f"{Colors.RED}🚫 No valid tokens found! Exiting...{Colors.RESET}")
            sys.exit()
        
        return valid_tokens

    def is_token_valid(self, token):
        """Check if token is valid"""
        try:
            url = f'https://graph.facebook.com/v17.0/me?access_token={token}'
            response = requests.get(url, timeout=10)
            return response.status_code == 200
        except:
            return False

    def get_user_info(self, token):
        """Get user info from token"""
        try:
            url = f'https://graph.facebook.com/v17.0/me?fields=name,id&access_token={token}'
            response = requests.get(url, timeout=10)
            data = response.json()
            return data.get('name', 'Unknown'), data.get('id', 'Unknown')
        except:
            return "Unknown", "Unknown"

    def load_comments(self):
        """Load comments from file or input"""
        print(f"\n{Colors.YELLOW}💬 Comment Source:{Colors.RESET}")
        print("1. Local file")
        print("2. GitHub URL")
        print("3. Direct input")
        
        choice = input(f"{Colors.GREEN}Choose (1/2/3): {Colors.RESET}").strip()
        comments = []
        
        if choice == "1":
            file_path = input(f"{Colors.GREEN}📁 Enter comments file: {Colors.RESET}").strip()
            if not file_path:
                file_path = "comments.txt"
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    comments = [line.strip() for line in f if line.strip()]
                print(f"{Colors.GREEN}✅ Loaded {len(comments)} comments{Colors.RESET}")
            except:
                print(f"{Colors.RED}❌ Cannot read comments file{Colors.RESET}")
                return self.load_comments()
        
        elif choice == "2":
            github_url = input(f"{Colors.GREEN}🔗 Enter GitHub raw URL: {Colors.RESET}").strip()
            try:
                response = requests.get(github_url, timeout=15)
                if response.status_code == 200:
                    comments = [line.strip() for line in response.text.split('\n') if line.strip()]
                    print(f"{Colors.GREEN}✅ Loaded {len(comments)} comments from GitHub{Colors.RESET}")
                else:
                    print(f"{Colors.RED}❌ Failed to load from GitHub{Colors.RESET}")
            except Exception as e:
                print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}")
        
        else:
            comment_text = input(f"{Colors.GREEN}📝 Enter comment text: {Colors.RESET}").strip()
            comments = [comment_text]
            print(f"{Colors.GREEN}✅ Using direct comment{Colors.RESET}")
        
        return comments

    def post_comment(self, token, post_id, comment):
        """Post comment to Facebook"""
        try:
            url = f"https://graph.facebook.com/v17.0/{post_id}/comments"
            headers = {
                'User-Agent': random.choice([
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36',
                    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/537.36'
                ]),
                'Authorization': f'Bearer {token}'
            }
            data = {
                'message': comment,
                'access_token': token
            }
            
            time.sleep(random.uniform(2, 5))
            
            response = requests.post(url, headers=headers, data=data, timeout=30)
            
            if response.status_code == 200:
                return True, "Success"
            else:
                error_data = response.json()
                error_msg = error_data.get('error', {}).get('message', 'Unknown error')
                return False, error_msg
                
        except requests.exceptions.Timeout:
            return False, "Timeout"
        except requests.exceptions.ConnectionError:
            return False, "Connection Error"
        except Exception as e:
            return False, f"Error: {str(e)}"

    def run_bot(self):
        """Main bot function"""
        clear_screen()
        show_banner()
        
        self.check_password()
        
        print(f"{Colors.CYAN}🕒 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.RESET}")
        print(f"{Colors.GREEN}{'═'*70}{Colors.RESET}")
        
        # Token source
        print(f"\n{Colors.YELLOW}🔑 TOKEN SOURCE:{Colors.RESET}")
        print("1. Local file (tokens.txt)")
        print("2. GitHub URL")
        print("3. Direct input")
        
        token_source = input(f"{Colors.GREEN}Choose (1/2/3): {Colors.RESET}").strip()
        tokens = self.load_tokens(token_source)
        
        if not tokens:
            print(f"{Colors.RED}❌ No tokens loaded!{Colors.RESET}")
            return
        
        # Validate tokens
        valid_tokens = self.validate_tokens(tokens)
        
        # Load comments
        comments = self.load_comments()
        if not comments:
            print(f"{Colors.RED}❌ No comments loaded!{Colors.RESET}")
            return
        
        # Get post ID
        post_id = input(f"\n{Colors.GREEN}🎯 Enter Post ID: {Colors.RESET}").strip()
        if not post_id:
            print(f"{Colors.Red}❌ Post ID required!{Colors.RESET}")
            return
        
        # Page token option
        print(f"\n{Colors.YELLOW}📄 PAGE TOKEN OPTION:{Colors.RESET}")
        use_page = input(f"{Colors.GREEN}Use page tokens? (y/n): {Colors.RESET}").lower().strip()
        page_ids = []
        
        if use_page == 'y' or use_page == 'yes':
            page_input = input(f"{Colors.GREEN}Enter Page IDs (comma separated): {Colors.RESET}").strip()
            page_ids = [pid.strip() for pid in page_input.split(',') if pid.strip()]
            print(f"{Colors.GREEN}✅ Using {len(page_ids)} page IDs{Colors.RESET}")
        
        # Safety settings
        print(f"\n{Colors.YELLOW}⚙️  SAFETY SETTINGS:{Colors.RESET}")
        try:
            min_delay = int(input(f"{Colors.GREEN}Min delay (seconds): {Colors.RESET}") or "120")
            max_delay = int(input(f"{Colors.GREEN}Max delay (seconds): {Colors.RESET}") or "300")
            
            if min_delay < 60:
                print(f"{Colors.RED}❌ Minimum delay should be 60+ seconds!{Colors.RESET}")
                return
        except:
            print(f"{Colors.RED}❌ Invalid delay input!{Colors.RESET}")
            return
        
        # Final confirmation
        print(f"\n{Colors.GREEN}{'═'*70}{Colors.RESET}")
        print(f"{Colors.CYAN}🎯 READY TO START:{Colors.RESET}")
        print(f"   🔑 Valid Tokens: {len(valid_tokens)}")
        print(f"   💬 Comments: {len(comments)}")
        print(f"   📝 Target Post: {post_id}")
        print(f"   ⏰ Delay: {min_delay}-{max_delay} seconds")
        
        if page_ids:
            print(f"   📄 Page IDs: {', '.join(page_ids)}")
        
        confirm = input(f"\n{Colors.YELLOW}🚀 Start commenting? (y/n): {Colors.RESET}").lower()
        if confirm != 'y':
            print(f"{Colors.RED}❌ Operation cancelled{Colors.RESET}")
            return
        
        # Start continuous commenting
        self.start_commenting(valid_tokens, post_id, comments, page_ids, min_delay, max_delay)

    def start_commenting(self, valid_tokens, post_id, comments, page_ids, min_delay, max_delay):
        """Start continuous commenting loop"""
        print(f"\n{Colors.GREEN}🚀 Starting continuous commenting...{Colors.RESET}")
        print(f"{Colors.YELLOW}📍 Press Ctrl+C to stop{Colors.RESET}")
        print(f"{Colors.GREEN}{'═'*70}{Colors.RESET}")
        
        success_count = 0
        fail_count = 0
        token_index = 0
        removed_tokens = 0
        
        try:
            while True:
                if not valid_tokens:
                    print(f"{Colors.RED}❌ All tokens are invalid! Stopping...{Colors.RESET}")
                    break
                
                current_token = valid_tokens[token_index % len(valid_tokens)]
                token_index += 1
                
                if not self.is_token_valid(current_token):
                    print(f"{Colors.RED}🗑️  Removing expired token{Colors.RESET}")
                    valid_tokens.remove(current_token)
                    removed_tokens += 1
                    print(f"{Colors.YELLOW}   📊 Remaining tokens: {len(valid_tokens)}{Colors.RESET}")
                    continue
                
                user_name, user_id = self.get_user_info(current_token)
                comment = random.choice(comments)
                
                target_post = post_id
                if page_ids and random.choice([True, False]):
                    page_id = random.choice(page_ids)
                    target_post = f"{page_id}_{post_id}"
                
                print(f"\n{Colors.CYAN}👤 User: {user_name}{Colors.RESET}")
                print(f"{Colors.WHITE}   🔑 Token: {current_token[:25]}...{Colors.RESET}")
                print(f"{Colors.WHITE}   📝 Target: {target_post}{Colors.RESET}")
                print(f"{Colors.WHITE}   💬 Comment: {comment[:60]}...{Colors.RESET}")
                
                success, error_msg = self.post_comment(current_token, target_post, comment)
                
                if success:
                    success_count += 1
                    print(f"{Colors.GREEN}   ✅ Comment posted successfully!{Colors.RESET}")
                else:
                    fail_count += 1
                    print(f"{Colors.RED}   ❌ Failed: {error_msg}{Colors.RESET}")
                    
                    if any(word in error_msg.lower() for word in ['token', 'expired', 'invalid', 'access']):
                        print(f"{Colors.RED}   🗑️  Removing invalid token{Colors.RESET}")
                        valid_tokens.remove(current_token)
                        removed_tokens += 1
                
                print(f"{Colors.BLUE}   📊 Stats: ✅{success_count} | ❌{fail_count} | 🔑{len(valid_tokens)} | 🗑️{removed_tokens}{Colors.RESET}")
                
                delay = random.randint(min_delay, max_delay)
                print(f"{Colors.YELLOW}   ⏳ Next comment in {delay} seconds...{Colors.RESET}")
                
                for remaining in range(delay, 0, -1):
                    if remaining % 30 == 0 or remaining <= 10:
                        print(f"{Colors.YELLOW}   ⏰ {remaining} seconds remaining...{Colors.RESET}", end='\r')
                    time.sleep(1)
                
                print(" " * 60, end='\r')
                
        except KeyboardInterrupt:
            print(f"\n\n{Colors.RED}🛑 Bot stopped by user{Colors.RESET}")
        
        print(f"\n{Colors.GREEN}{'═'*70}{Colors.RESET}")
        print(f"{Colors.CYAN}📊 FINAL REPORT:{Colors.RESET}")
        print(f"{Colors.GREEN}   ✅ Successful Comments: {success_count}{Colors.RESET}")
        print(f"{Colors.RED}   ❌ Failed Comments: {fail_count}{Colors.RESET}")
        print(f"{Colors.BLUE}   🔑 Valid Tokens Remaining: {len(valid_tokens)}{Colors.RESET}")
        print(f"{Colors.YELLOW}   🗑️  Tokens Removed During Runtime: {removed_tokens}{Colors.RESET}")
        print(f"{Colors.MAGENTA}   🕒 Ended: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.RESET}")
        print(f"{Colors.GREEN}{'═'*70}{Colors.RESET}")

def main():
    try:
        bot = FacebookCommentBot()
        bot.run_bot()
    except Exception as e:
        print(f"{Colors.RED}💥 Critical error: {e}{Colors.RESET}")

if __name__ == "__main__":
    main()
