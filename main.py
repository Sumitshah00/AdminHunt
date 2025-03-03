import requests
import random
import time
import webbrowser
from colorama import Fore, Style, init
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import logging
import argparse
import os
import subprocess
import sys
import atexit

# Initialize colorama
init(autoreset=True)

# Logging setup
logging.basicConfig(filename='hacksagex_admin_finder.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(message)s')

# Custom colors
PURPLISH_PINK = "\033[95m"
RED_SKY_BLUE = "\033[96m"

# Banner
banner = r"""
⠀⠀⢀⣠⣶⣾⣿⣿⣿⣶⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠴⠚⠛⠛⠳⢶⣄⡀⠀⠀
⠀⣠⣿⡿⠛⠉⠁⠀⠉⠙⠻⣿⣷⡀⠀⠀⣠⣴⡶⠀⠀⠀⠀⠀⠀⠀⠙⢿⣄⠀
⢰⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⡄⣸⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⡆
⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣽⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣷
⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⢯⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⡟
⠸⣿⣧⡀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⠃⠙⣿⣷⡄⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⠃
⠀⠙⢿⣿⣦⣀⣀⢀⣀⣠⣶⣿⠟⠁⠀⠀⠈⠻⣿⣶⣄⣀⡀⢀⣀⣤⣾⡿⠃⠀
⠀⠀⠀⠙⠻⠿⠿⠿⠿⠿⠛⠁⠀⠀⠀⠀⠀⠀⠈⠛⠿⢿⣿⣿⠿⠟⠉⠀⠀⠀
"""

# Tool information
developer_info = f"{RED_SKY_BLUE}> Developer: HackSageX <{Style.RESET_ALL}"
version_info = f"{RED_SKY_BLUE}> Version: 2.5.0 <{Style.RESET_ALL}"
about_tool = f"""
{RED_SKY_BLUE}> About: HackSageX Admin Finder is a powerful tool designed to discover admin panels on a target website by brute-forcing directories and files specified in a wordlist. It supports multithreading, Tor IP rotation, and CAPTCHA handling for efficient scanning. <{Style.RESET_ALL}
"""

# User agent list
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 11; Pixel 4 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101 Firefox/90.0"
]

# Tor settings
TOR_PORT = 9050
TOR_CONTROL_PORT = 9051
TOR_PASSWORD = "your_password"  # Set a password for Tor control port
TOR_PROCESS = None  # Global variable to store the Tor process

# Default settings
DEFAULT_DELAY = 1  # Delay between requests
DEFAULT_THREADS = 10  # Number of threads
DEFAULT_TIMEOUT = 10  # Request timeout


def animate_banner(banner):
    for line in banner.splitlines():
        if line.strip():
            print(PURPLISH_PINK + line + Style.RESET_ALL)
            time.sleep(0.1)


def read_wordlist(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]


def start_tor():
    """Start Tor in a new terminal window."""
    global TOR_PROCESS
    try:
        if sys.platform == "win32":
            # Windows
            TOR_PROCESS = subprocess.Popen(["start", "cmd", "/k", "tor"],
                                           shell=True)
        elif sys.platform == "darwin":
            # macOS
            TOR_PROCESS = subprocess.Popen(["open", "-a", "Terminal", "tor"])
        else:
            # Linux
            TOR_PROCESS = subprocess.Popen(
                ["x-terminal-emulator", "-e", "tor"])
        print(Fore.GREEN + "Tor started in a new terminal window." +
              Style.RESET_ALL)
        time.sleep(5)  # Wait for Tor to initialize
    except Exception as e:
        print(Fore.RED + f"Failed to start Tor: {e}" + Style.RESET_ALL)
        sys.exit(1)


def stop_tor():
    """Stop the Tor process."""
    global TOR_PROCESS
    if TOR_PROCESS:
        TOR_PROCESS.terminate()
        print(Fore.GREEN + "Tor process terminated." + Style.RESET_ALL)


def renew_tor_ip():
    """Renew Tor IP by sending a signal to the Tor control port."""
    with Controller.from_port(port=TOR_CONTROL_PORT) as controller:
        controller.authenticate(password=TOR_PASSWORD)
        controller.signal(Signal.NEWNYM)
    print(Fore.CYAN + "Renewed Tor IP address." + Style.RESET_ALL)


def get_tor_session():
    """Create a requests session that uses Tor."""
    session = requests.Session()
    session.proxies = {
        'http': f'socks5h://127.0.0.1:{TOR_PORT}',
        'https': f'socks5h://127.0.0.1:{TOR_PORT}',
    }
    try:
        # Test Tor connection
        test_url = "https://check.torproject.org"
        response = session.get(test_url, timeout=10)
        if "Congratulations" in response.text:
            print(Fore.GREEN + "Tor is working correctly." + Style.RESET_ALL)
        else:
            print(Fore.RED +
                  "Tor is not working. Please check your Tor configuration." +
                  Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Tor connection failed: {e}" + Style.RESET_ALL)
    return session


def page_has_error(content):
    error_indicators = [
        "error", "not found", "404", "page not available", "Oops!"
    ]
    return any(indicator.lower() in content.lower()
               for indicator in error_indicators)


def check_url(url, session, headers, timeout):
    try:
        response = session.get(url, headers=headers, timeout=timeout)
        logging.info(f"Checking {url}... Status code: {response.status_code}")

        if response.status_code == 200 and response.url == url and not page_has_error(
                response.text):
            print(Fore.GREEN + f"Valid admin panel found: {url}" +
                  Style.RESET_ALL)
            return url
        elif response.status_code == 403:
            print(
                Fore.GREEN +
                f"403 Forbidden: {url}.  potentially  an admin panel or a CAPTCHA..." +
                Style.RESET_ALL)
            webbrowser.open(url)
            input(Fore.YELLOW + "Press Enter after solving CAPTCHA..." +
                  Style.RESET_ALL)
            response = session.get(url, headers=headers, timeout=timeout)
            if response.status_code == 200 and response.url == url and not page_has_error(
                    response.text):
                print(Fore.GREEN +
                      f"Valid admin panel found (after CAPTCHA): {url}" +
                      Style.RESET_ALL)
                return url
            else:
                print(Fore.RED +
                      f"Still 403 Forbidden after solving CAPTCHA: {url}" +
                      Style.RESET_ALL)
        elif response.status_code == 404 or page_has_error(response.text):
            print(Fore.RED + f"404 Not Found or error detected: {url}" +
                  Style.RESET_ALL)
        else:
            print(Fore.YELLOW +
                  f"Received status code: {response.status_code}" +
                  Style.RESET_ALL)

    except requests.ConnectionError:
        print(Fore.RED +
              "Error: Connection failed. Check your internet connection." +
              Style.RESET_ALL)
    except requests.Timeout:
        print(Fore.RED + "Error: Request timed out." + Style.RESET_ALL)
    except requests.RequestException as e:
        print(Fore.RED + f"Error checking {url}: {e}" + Style.RESET_ALL)

    return None


def check_valid_url(base_url, word_list, threads, delay, timeout):
    session = get_tor_session()
    base_url = base_url.rstrip("/")
    valid_urls = []

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = []
        for word in word_list:
            if word.isdigit():  # Handle ports
                url = f"{base_url}:{word}"
            else:  # Handle paths
                url = f"{base_url}/{word}"
            headers = {
                'User-Agent': random.choice(USER_AGENTS),
                'Referer': base_url,
                'Accept':
                'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
            }
            futures.append(
                executor.submit(check_url, url, session, headers, timeout))
            time.sleep(delay)

        for future in tqdm(as_completed(futures),
                           total=len(word_list),
                           desc="Scanning URLs"):
            result = future.result()
            if result:
                valid_urls.append(result)
            renew_tor_ip()  # Renew Tor IP after each request

    return valid_urls


def display_ascii_art():
    animate_banner(banner)
    print(developer_info)
    print(version_info)
    print(about_tool)


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


def main():
    display_ascii_art()

    # Start Tor automatically
    start_tor()
    atexit.register(stop_tor)  # Stop Tor when the script exits

    parser = argparse.ArgumentParser(
        description=
        "HackSageX Admin Finder - Discover admin panels on a target website.")
    parser.add_argument("-u", "--url", help="Base URL to scan", required=True)
    parser.add_argument("-w",
                        "--wordlist",
                        help="Path to wordlist file",
                        default="wordlist.txt")
    parser.add_argument("-t",
                        "--threads",
                        help="Number of threads",
                        type=int,
                        default=DEFAULT_THREADS)
    parser.add_argument("-d",
                        "--delay",
                        help="Delay between requests (seconds)",
                        type=float,
                        default=DEFAULT_DELAY)
    parser.add_argument("-to",
                        "--timeout",
                        help="Request timeout (seconds)",
                        type=int,
                        default=DEFAULT_TIMEOUT)
    args = parser.parse_args()

    if not is_valid_url(args.url):
        print(Fore.RED + "Invalid URL. Please enter a valid URL." +
              Style.RESET_ALL)
        return

    try:
        word_list = read_wordlist(args.wordlist)
        if not word_list:
            print(Fore.RED +
                  "Wordlist is empty. Please provide a valid wordlist." +
                  Style.RESET_ALL)
            return

        print(
            Fore.CYAN +
            f"Starting scan with {args.threads} threads and {args.delay}s delay..."
            + Style.RESET_ALL)
        valid_urls = check_valid_url(args.url, word_list, args.threads,
                                     args.delay, args.timeout)

        if valid_urls:
            print(
                Fore.GREEN +
                f"Finished scanning. Valid admin panels found: {len(valid_urls)}"
                + Style.RESET_ALL)
            for url in valid_urls:
                print(Fore.GREEN + f"- {url}" + Style.RESET_ALL)
        else:
            print(Fore.RED + "No valid admin panels found." + Style.RESET_ALL)

    except FileNotFoundError:
        print(Fore.RED + f"Wordlist file not found: {args.wordlist}" +
              Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"An error occurred: {e}" + Style.RESET_ALL)

    # Display example command
    print(
        Fore.RED +
        "\nExample Command: python main.py -u http://example.com -w wordlist.txt -t 20 -d 0.5 -to 15"
        + Style.RESET_ALL)
    print(Fore.RED + "> -u: Target URL (e.g., http://example.com)" +
          Style.RESET_ALL)
    print(Fore.RED + "> -w: Path to wordlist file (default: wordlist.txt)" +
          Style.RESET_ALL)
    print(Fore.RED + "> -t: Number of threads (default: 10)" + Style.RESET_ALL)
    print(Fore.RED + "> -d: Delay between requests in seconds (default: 1)" +
          Style.RESET_ALL)
    print(Fore.RED + "> -to: Request timeout in seconds (default: 10)" +
          Style.RESET_ALL)


if __name__ == "__main__":
    main()
