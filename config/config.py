from web3 import Web3


MINTING_CONTRACT = "0x9C868614ffca7da36B36330b1f317B117c7834dE"
MINTING_CONTRACT_ABI = '[{"constant":false,"inputs":[{"name":"to","type":"address"},{"name":"amount","type":"uint256"}],"name":"mint","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]'


CHAIN = {
    "SEPOLIA": {
        "RPC": 'https://base-sepolia-rpc.publicnode.com',
        "EXPLORER": "https://base-sepolia.blockscout.com",
        "CONTRACT_ADDRESS":"0xAFdF5cb097D6FB2EB8B1FFbAB180e667458e18F4",
        "CHAIN_ID": 84532,
    },
    
}


TOKENS = {
   
    "ETH": {"address": None, "decimals": 18},
    "USDC": {"address": "0x9C868614ffca7da36B36330b1f317B117c7834dE", "decimals": 6},
}
WRAP_CONTRACT = "0x50930beB58690a21c528dC351d6818F51CAfA480"

WRAP_ABI = '[{"type":"function","name":"wrap","inputs":[{"name":"amount","type":"uint256"}],"outputs":[],"stateMutability":"payable"}]'


ERC20_ABI = '[{"constant":true,"inputs":[{"name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"type":"function"},{"constant":false,"inputs":[{"name":"spender","type":"address"},{"name":"amount","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"type":"function"},{"constant":true,"inputs":[{"name":"owner","type":"address"},{"name":"spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"type":"function"}]'

