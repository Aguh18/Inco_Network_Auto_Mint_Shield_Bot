from web3 import Web3

from display import logging
from eth_account import Account
from config import config
from dotenv import load_dotenv
from display import appearance
from utils.utils import show_balance
from utils.utils import check_connection
from utils.utils import wait_until_next_day
from utils.utils import mint
from utils.utils import wrap
import os

load_dotenv()


def main():
    print(appearance.ASCII_ART)
    print(appearance.CREDIT)
    
    PRIVATE_KEY = os.getenv("PRIVATE_KEY") 
    account = Account.from_key('0x' + PRIVATE_KEY)
    address = account.address
    web3 = Web3(Web3.HTTPProvider(config.CHAIN["SEPOLIA"]["RPC"]))
    logging.log_info(f"Account Address: {address}")
    
    logging.log_info("Connecting to Sepolia node...")
    is_connect = check_connection(web3)
    if not is_connect:
        logging.log_error("Failed to connect to Sepolia node")
        return

    print("-"*50)
    logging.log_success("Connected to both nodes successfully!")
    
    print("CHECKING BALANCE...")
    print("-"*50)
    show_balance(address, web3, token="ETH", chain="SEPOLIA")
    show_balance(address, web3, token="USDC", chain="SEPOLIA")
    
    
    

    # Menu
    
    while True:
        print("-"*50)
        logging.log_info("1. Mint")
        logging.log_info("2. shied")
        logging.log_info("3. Auto Mode")
        logging.log_info("4. check balance")
        logging.log_info("5. Exit")
        print("-"*50)
        
        choice = input("Enter your choice: ")
        if choice == "1" or choice == "2":
            amount = int(input("Enter the amount to mint/shield: "))
            process_count = int(input("Enter the number of processes to run: "))
            if choice == "1":
                success_count = 0
                logging.log_info("Minting...")
                for i in range(process_count):
                    print("-"*50)
                    if mint(PRIVATE_KEY, web3, amount):
                        success_count += 1
                logging.log_success(f"minting completed! {success_count} transactions successful.")
                continue
            elif choice == "2":
                success_count = 0
                logging.log_info("shield...")
                for i in range(process_count):
                    print("-"*50)
                    if wrap(PRIVATE_KEY, web3, amount):
                        success_count += 1
                logging.log_success(f"minting completed! {success_count} transactions successful.")
                continue
        elif choice == "3":
            mode = input("do you want to run automaticly every day /once [auto/once]: ")
            if mode not in ["auto", "once"]:
                logging.log_error("Invalid mode. Please choose 'auto' or 'once'.")
                continue
            amount = int(input("Enter the amount to mint/shield: "))
            process_count = int(input("Enter the number of processes to run: "))
            while True:
                success_count = 0
                print("-"*50)
                logging.log_info("Minting...")
                for i in range(process_count):
                    print("-"*50)
                    if mint(PRIVATE_KEY, web3, amount):
                        success_count += 1
                logging.log_success(f"minting completed! {success_count} transactions successful.")
                success_count = 0
                print
                logging.log_info("shield...")
                for i in range(process_count):
                    print("-"*50)
                    if wrap(PRIVATE_KEY, web3, amount):
                        success_count += 1
                logging.log_success(f"shield completed! {success_count} transactions successful.")
                if mode == "once":
                    break
                elif mode == "auto":
                    print("-"*50)
                    wait_until_next_day()
                    continue
            continue
        elif choice == "4":
            print("-"*50)
            logging.log_info("Checking balance...")
            show_balance(address, web3, token="ETH", chain="SEPOLIA")
            show_balance(address, web3, token="USDC", chain="SEPOLIA")
            print("-"*50)
            continue
            
        elif choice == "5":
            logging.log_info("Exiting...")
            break
        else:
            logging.log_error("Invalid choice. Please try again.")
            
   
    
    
    
if __name__ == "__main__":
    try:
        
        main()
    except KeyboardInterrupt:
        logging.log_warning("Program interrupted by user.")
        
        





