<p align="center">
  <img src="https://github.com/Sumitshah00.png" width="150" height="150" style="border-radius: 50%;" alt="Profile Picture"/>
</p>
<p align="center">
  <img src="https://img.shields.io/github/stars/Sumitshah00/AdminHunt?style=for-the-badge" alt="Stars">
  <img src="https://img.shields.io/github/forks/Sumitshah00/AdminHunt?style=for-the-badge" alt="Forks">
  <img src="https://img.shields.io/github/license/Sumitshah00/AdminHunt?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/github/issues/Sumitshah00/AdminHunt?style=for-the-badge" alt="Issues">
  <br>
  <img src="https://komarev.com/ghpvc/?username=Sumitshah00&color=blue&style=flat" alt="Repo Views">
</p>

# HackSageX Admin Finder 🚀

HackSageX Admin Finder is a powerful tool designed to discover admin panels on a target website by brute-forcing directories and files specified in a wordlist. It supports multithreading, Tor IP rotation, and CAPTCHA handling for efficient scanning.

## ✨ Features
✅ Multithreaded scanning for fast results  
✅ Supports Tor for anonymity and IP rotation  
✅ CAPTCHA handling for restricted admin panels  
✅ Logs results for further analysis  
✅ Customizable delay and timeout settings  
✅ Randomized User-Agents to evade detection  

---

## 🛠️ Installation

### Prerequisites
Ensure you have the following installed on your system:
- Python 3.x
- Tor (for IP rotation)
- Required Python libraries:
  ```sh
 pip install requests colorama tqdm argparse --break-system-packages
  ```

### Cloning the Repository
```sh
git clone https://github.com/Sumitshah00/AdminHunt.git
cd AdminHunt
```

---

## 🚀 Usage
### Basic Command
```sh
python main.py -u <target_url> -w <wordlist.txt>
```

### Options
| Option       | Description                                  |
|-------------|------------------------------------------|
| `-u, --url` | Target website URL to scan              |
| `-w, --wordlist` | Path to wordlist file containing admin panel paths |
| `-t, --threads` | Number of concurrent threads (default: 10) |
| `-d, --delay` | Delay between requests (default: 1s) |
| `--tor` | Enable Tor for anonymity |

### Example
```sh
python main.py -u https://example.com -w admin_wordlist.txt -t 20 --tor
```

---

## 🥷 Tor Configuration (Optional)
To use Tor, ensure it is installed and running:
- Start Tor:
  ```sh
  tor
  ```
- Use `--tor` in the command to enable Tor IP rotation.

---

## 🐜 Logging
All scan results are saved in `hacksagex_admin_finder.log` for future reference.

---

## ⚠️ Disclaimer
> **This tool is intended for educational and authorized penetration testing purposes only.** Use it responsibly and only on systems you have permission to test.

---

## 🧑‍💻 Developer
Developed by [HackSageX](https://github.com/Sumitshah00). If you find this tool useful, consider giving it a ⭐!
             [HackSageX](https://instagram.com/hacksagex). you can follow me on my instagram
<p align="center">
![image](https://github.com/user-attachments/assets/547d3fe5-aa1a-43aa-8796-94fd5146b30e)
</p>

---

