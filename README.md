# AdminHunt

AdminHunt is a Python script that automates the search for a website's admin panel by iterating through potential paths specified in a wordlist. It rotates IP addresses, handles CAPTCHA challenges, and randomizes user-agents to minimize detection, making it a valuable tool for penetration testers and ethical hackers.

## Features

- **Banner Animation**: Displays an ASCII banner on startup for a dynamic look.
- **Wordlist Options**: Select from a default wordlist or specify a custom one for flexibility in scanning.
- **User-Agent Randomization**: Avoids detection by using random User-Agent headers.
- **IP Rotation**: Changes IP address after each request to evade rate limits.
- **CAPTCHA Handling**: Opens the browser for manual CAPTCHA solving if a 403 Forbidden error is encountered.
- **Detailed Status Feedback**: Indicates the HTTP status for each URL checked and identifies valid admin pages.
- **Error Detection**: Detects common error indicators like "404 Not Found" or "Error" pages.

## Requirements

- Python 3.x
- Required packages:
  - `requests`
  - `colorama`

# Install the necessary packages by running:

```pip install requests colorama```

# How to Use
Clone the Repository:
```git clone https://github.com/Sumitshah00/AdminHunt.git```
```cd AdminHunt```

# Run the Script:

```python main.py```

# Example Output

██████╗ ██╗   ██╗████████╗███████╗ █████╗ ███████╗███████╗ █████╗ ███████╗███████╗██╗███╗   ██╗███████╗
██╔══██╗╚██╗ ██╔╝╚══██╔══╝██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗██╔════╝██╔════╝██║████╗  ██║██╔════╝
██████╔╝ ╚████╔╝    ██║   █████╗  ███████║███████╗███████╗███████║███████╗███████╗██║██╔██╗ ██║███████╗
██╔══██╗  ╚██╔╝     ██║   ██╔══╝  ██╔══██║███████║███████║██╔══██║███████║███████║██║██║╚██╗██║╚════██║
██████╔╝   ██║      ██║   ███████╗██║  ██║╚════██║╚════██║██║  ██║╚════██║╚════██║██║██║ ╚████║███████║
╚═════╝    ╚═╝      ╚═╝   ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝╚═╝  ╚═══╝╚══════╝
> Developer: @byteassassins <
> Version: 1.1.0 <

Enter the website URL (e.g., http://example.com): http://example.com
Choose a wordlist option:
1. Default wordlist (wordlist.txt in the same folder)
2. Custom wordlist (provide the path

# Enter the Target URL:

When prompted, input the base URL of the target website, e.g., http://example.com.

# Select the Wordlist:

Option 1: Use the default wordlist.txt included in the directory.
Option 2: Provide a custom wordlist file path for scanning specific paths.

# View Results: 

The script will attempt to find the admin panel by checking each path in the wordlist, reporting any accessible pages with HTTP status codes.

# Contributing

Feel free to fork the repository and submit issues or pull requests to contribute to the project.

“Developer Information --------------------- * **Author**: [Sumitshah00](https://github.com/Sumitshah00) * **Instagram**: [@byteassassins](https://www.instagram.com/byteassassins/)”


