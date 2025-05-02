from colorama import Fore, Style

from colorama import Fore, Style, init

# Inisialisasi colorama agar bekerja di terminal Windows dan lainnya
init(autoreset=True)

def log_info(message):
    print(f"{Fore.CYAN}[INFO] {message}")

def log_success(message):
    print(f"{Fore.GREEN}[SUCCESS] {message}")

def log_warning(message):
    print(f"{Fore.YELLOW}[WARNING] {message}")

def log_error(message):
    print(f"{Fore.RED}[ERROR] {message}")

def log_debug(message):
    print(f"{Fore.MAGENTA}[DEBUG] {message}")

def log_critical(message):
    print(f"{Fore.LIGHTRED_EX}[CRITICAL] {message}")

def log_fatal(message):
    print(f"{Fore.RED + Style.BRIGHT}[FATAL] {message}")

def log_trace(message):
    print(f"{Fore.BLUE}[TRACE] {message}")
