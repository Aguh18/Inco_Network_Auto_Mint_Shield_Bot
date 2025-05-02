from web3 import Web3
from display import logging

from config import config

import time
import random
from datetime import datetime, timedelta


def wait_until_next_day():
    now = datetime.now()

    # Random waktu antara jam 14:00 sampai 17:00
    random_hour = random.randint(14, 17)
    random_minute = random.randint(0, 59)
    random_second = random.randint(0, 59)

    next_run_time = datetime(now.year, now.month, now.day, random_hour, random_minute, random_second)

    # Cek apakah waktu sekarang > next_run_time atau selisihnya < 8 jam
    if now > next_run_time or (next_run_time - now).total_seconds() < 8 * 60 * 60:
        next_run_time += timedelta(days=1)

    # Log jadwal berikutnya menggunakan f-string
    logging.log_info(f"Next run scheduled at {next_run_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    while True:
        now = datetime.now()
        time_remaining = next_run_time - now

        if time_remaining.total_seconds() <= 0:
            break

        # Tampilkan countdown menggunakan print karena logging tidak mendukung end='\r'
        countdown = str(time_remaining).split('.')[0]
        print(f"Countdown: {countdown}", end='\r')
        time.sleep(1)

    # Newline dan pesan sukses menggunakan logging
    print
    logging.log_info(f"('It is now time to run the next transaction!'")

def check_connection(web3):
    try:
        # Check if connected
        if web3.is_connected():
            logging.log_success("Connected to  node")
            return True
        else:
            logging.log_error("Failed to connect to  node")
            return False
    except Exception as e:
        logging.log_error(f"Error checking connection: {e}")
        return False

def is_valid_address(address):
    return Web3.is_checksum_address(address)


def check_token_balance(address, web3, token=None):
    try:
        if not web3.is_address(address):
            raise ValueError("Invalid Ethereum address")

        address = web3.to_checksum_address(address)

        if token:
            token_data = config.TOKENS.get(token)
         
            if not token_data:
                raise ValueError(f"Token '{token}' not found in config")

            token_contract = web3.eth.contract(address=web3.to_checksum_address(token_data["address"]), abi=config.ERC20_ABI)
            raw_balance = token_contract.functions.balanceOf(address).call()
            decimals = token_data.get("decimals", 18)
            balance = raw_balance / 10**decimals
            return balance
        
        decimals= config.TOKENS["ETH"]["decimals"]
        raw_eth_balance = web3.eth.get_balance(address)
        eth_balance = raw_eth_balance / 10**decimals
        return eth_balance

    except Exception as e:
        logging.log_error(f"Error checking balance: {e}")
        return None

    
def show_balance(address, web3, token=None, chain=None):
    if token and token != "ETH":
        balance = check_token_balance(address, web3, token)
        if balance is not None:
            logging.log_info(f"{chain} {token} Balance: {balance:.18f}  {token}")
           
    else:
        balance = check_token_balance(address, web3)
        logging.log_info(f"{chain} ETH Balance: {balance:.18f} ETH".rstrip('0').rstrip('.'))
        
  
def mint(private_key, w3, amount):
    try:
        logging.log_info(f"Minting {amount} USDC...")
       
        account = w3.eth.account.from_key(private_key)
        wallet_address = account.address
        # Gunakan 'pending' untuk memasukkan transaksi tertunda
        nonce = w3.eth.get_transaction_count(wallet_address, "pending")
        # Jumlah dalam USDC (misalnya, 1 USDC jika 6 desimal)
        

        # Inisialisasi kontrak
        contract = w3.eth.contract(address=config.MINTING_CONTRACT, abi=config.MINTING_CONTRACT_ABI)

        # Estimasi gas dengan buffer
        gas_estimate = contract.functions.mint(
            w3.to_checksum_address(wallet_address),
            amount
        ).estimate_gas({"from": wallet_address})
        gas_estimate = int(gas_estimate * 1.2)  # Tambah 20% buffer
        logging.log_debug(f"Gas estimate: {gas_estimate}")

        # Gas price dinamis dengan buffer
        gas_price = int(w3.eth.gas_price *1.3)  # Tambah 30% dari gas price jaringan
        logging.log_debug(f"Gas price: {w3.from_wei(gas_price, 'gwei')} gwei")

        # Membuat transaksi
        tx = contract.functions.mint(
            w3.to_checksum_address(wallet_address),
            amount
        ).build_transaction({
            "from": w3.to_checksum_address(wallet_address),
            "nonce": nonce,
            "gas": gas_estimate,
            "gasPrice": gas_price
        })

        # Menandatangani transaksi
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)

        # Mengirim transaksi
        
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

        # Menunggu konfirmasi
        logging.log_debug(f"Waiting for transaction receipt: {w3.to_hex(tx_hash)}")
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        # Cek status transaksi
        if tx_receipt.status == 1:
            logging.log_success(f"Transaction success! Tx Hash: {w3.to_hex(tx_hash)}")
            
        else:
            logging.log_error(f"Transaction failed! Tx Hash: {w3.to_hex(tx_hash)}")
            
        return True
    except Exception as e:
        logging.log_error(f"Error bridge: {str(e)}")
        return False



def approve(private_key, w3, spender_address, amount=1000000):
    try:
        
        
        account = w3.eth.account.from_key(private_key)
        wallet_address = account.address
        nonce = w3.eth.get_transaction_count(wallet_address, "pending")
        contract = w3.eth.contract(address=config.TOKENS['USDC']['address'], abi=config.ERC20_ABI)

        # Estimasi gas dengan buffer
        gas_estimate = contract.functions.approve(
            w3.to_checksum_address(spender_address),
            amount
        ).estimate_gas({"from": wallet_address})
        gas_estimate = int(gas_estimate * 1.2)  
    

        # Gas price dinamis dengan buffer
        gas_price = int(w3.eth.gas_price * 1.3)  
       

        
        tx = contract.functions.approve(
            w3.to_checksum_address(spender_address),
            amount
        ).build_transaction({
            "from": w3.to_checksum_address(wallet_address),
            "nonce": nonce,
            "gas": gas_estimate,
            "gasPrice": gas_price
        })

        signed_tx = w3.eth.account.sign_transaction(tx, private_key)

        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        return True
    except Exception as e:
        logging.log_error(f"Error approve: {str(e)}")
        return False
    
    
def wrap(private_key, w3, amount):
    try:
        
        account = w3.eth.account.from_key(private_key)
        wallet_address = account.address
        
        
        logging.log_info(f"Executing approve for amount: {amount}")
        approve_success = approve(private_key, w3,"0x50930beB58690a21c528dC351d6818F51CAfA480", amount)  
        if not approve_success:
            logging.log_error("Approve transaction failed")
            return False
        logging.log_success("Approve transaction successful")
      
        
        nonce = w3.eth.get_transaction_count(wallet_address, "pending")
    
        contract = w3.eth.contract(address=config.WRAP_CONTRACT, abi=config.WRAP_ABI)

        gas_estimate = contract.functions.wrap(
            amount
        ).estimate_gas({"from": wallet_address})
        gas_estimate = int(gas_estimate * 1.2)  
        logging.log_debug(f"Gas estimate: {gas_estimate}")

      
        gas_price = int(w3.eth.gas_price *1.3)  
        logging.log_debug(f"Gas price: {w3.from_wei(gas_price, 'gwei')} gwei")

        
        tx = contract.functions.wrap(
            amount
        ).build_transaction({
            "from": w3.to_checksum_address(wallet_address),
            "nonce": nonce,
            "gas": gas_estimate,
            "gasPrice": gas_price
        })

       
       
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)

       
        
        
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

       
        logging.log_debug(f"Waiting for transaction receipt: {w3.to_hex(tx_hash)}")
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

       
        if tx_receipt.status == 1:
            logging.log_success(f"Transaction success! Tx Hash: {w3.to_hex(tx_hash)}")
            
        else:
            logging.log_error(f"Transaction failed! Tx Hash: {w3.to_hex(tx_hash)}")
           
        return True
    except Exception as e:
        logging.log_error(f"Error bridge: {str(e)}")
  
        return False






    
