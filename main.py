import requests
import random
import time
import webbrowser
from colorama import Fore, Style, init
import re

# Initialize colorama
init(autoreset=True)

PURPLISH_PINK = "\033[95m"
RED_SKY_BLUE = "\033[96m"

banner = r"""
██████╗ ██╗   ██╗████████╗███████╗ █████╗ ███████╗███████╗ █████╗ ███████╗███████╗██╗███╗   ██╗███████╗
██╔══██╗╚██╗ ██╔╝╚══██╔══╝██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗██╔════╝██╔════╝██║████╗  ██║██╔════╝
██████╔╝ ╚████╔╝    ██║   █████╗  ███████║███████╗███████╗███████║███████╗███████╗██║██╔██╗ ██║███████╗
██╔══██╗  ╚██╔╝     ██║   ██╔══╝  ██╔══██║╚════██║╚════██║██╔══██║╚════██║╚════██║██║██║╚██╗██║╚════██║
██████╔╝   ██║      ██║   ███████╗██║  ██║███████║███████║██║  ██║███████║███████║██║██║ ╚████║███████║
╚═════╝    ╚═╝      ╚═╝   ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝╚═╝  ╚═══╝╚══════╝
"""

def animate_banner(banner):
    for line in banner.splitlines():
        if line.strip():
            print(PURPLISH_PINK + line + Style.RESET_ALL)
            time.sleep(0.1)

developer_info = f"{RED_SKY_BLUE}> Developer: @byteassassins <{Style.RESET_ALL}"
version = f"{RED_SKY_BLUE}> Version: 1.1.0 <{Style.RESET_ALL}"

# User agent list with a few common user agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 11; Pixel 4 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101 Firefox/90.0"
]

def read_wordlist(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def change_ip():
    print(Fore.CYAN + "Changing IP address..." + Style.RESET_ALL)
    time.sleep(1)

def page_has_error(content):
    """Detects if the page content likely represents an error page."""
    error_indicators = ["error", "not found", "404", "page not available", "Oops!"]
    return any(indicator.lower() in content.lower() for indicator in error_indicators)

def check_valid_url(base_url, word_list):
    session = requests.Session()
    base_url = base_url.rstrip("/")

    for word in word_list:
        url = f"{base_url}/{word}"
        print(Fore.YELLOW + f"Checking {url}..." + Style.RESET_ALL)

        headers = {
            'User-Agent': random.choice(USER_AGENTS),
            'Referer': base_url,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }

        try:
            response = session.get(url, headers=headers, timeout=10)
            print(Fore.BLUE + f"Status code: {response.status_code}" + Style.RESET_ALL)

            # Verify if the response URL is the same as the original to detect redirects
            if response.status_code == 200 and response.url == url and not page_has_error(response.text):
                print(Fore.GREEN + f"Valid URL found: {url}" + Style.RESET_ALL)
                return url
            elif response.status_code == 403:
                print(Fore.RED + f"403 Forbidden: {url}. Opening browser to solve CAPTCHA..." + Style.RESET_ALL)
                webbrowser.open(url)
                input(Fore.YELLOW + "Press Enter after solving CAPTCHA..." + Style.RESET_ALL)
                response = session.get(url, headers=headers, timeout=10)
                if response.status_code == 200 and response.url == url and not page_has_error(response.text):
                    print(Fore.GREEN + f"Valid URL found (after CAPTCHA): {url}" + Style.RESET_ALL)
                    return url
                else:
                    print(Fore.RED + f"Still 403 Forbidden after solving CAPTCHA: {url}" + Style.RESET_ALL)
            elif response.status_code == 404 or page_has_error(response.text):
                print(Fore.RED + f"404 Not Found or error detected: {url}" + Style.RESET_ALL)
            else:
                print(Fore.YELLOW + f"Received status code: {response.status_code}" + Style.RESET_ALL)

        except requests.ConnectionError:
            print(Fore.RED + "Error: Connection failed. Check your internet connection." + Style.RESET_ALL)
        except requests.Timeout:
            print(Fore.RED + "Error: Request timed out." + Style.RESET_ALL)
        except requests.RequestException as e:
            print(Fore.RED + f"Error checking {url}: {e}" + Style.RESET_ALL)

        change_ip()
        time.sleep(1)

    return None

def display_ascii_art():
    animate_banner(banner)
    print(developer_info)
    print(version)

def is_valid_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,})|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

display_ascii_art()

while True:
    base_url = input("Enter the website URL (e.g., http://example.com): ").strip()
    if not is_valid_url(base_url):
        print(Fore.RED + "Invalid URL. Please enter a valid URL." + Style.RESET_ALL)
        continue

    wordlist_choice = input("Choose a wordlist option:\n1. Default wordlist (wordlist.txt in the same folder)\n2. Custom wordlist (provide the path to your wordlist file)\nEnter 1 or 2: ")
    
    if wordlist_choice == '1':
        wordlist_file = 'wordlist.txt'
    elif wordlist_choice == '2':
        wordlist_file = input("Enter the path to your wordlist file: ").strip()
    else:
        print(Fore.RED + "Invalid choice. Please enter 1 or 2." + Style.RESET_ALL)
        continue

    try:
        word_list = read_wordlist(wordlist_file)
        found_url = check_valid_url(base_url, word_list)
        if found_url:
            print(Fore.GREEN + f"Finished searching. Valid URL found: {found_url}" + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "No valid URLs found." + Style.RESET_ALL)
    except FileNotFoundError:
        print(Fore.RED + f"Wordlist file not found: {wordlist_file}" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"An error occurred: {e}" + Style.RESET_ALL)
