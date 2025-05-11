# Inco Network bot

This script provides a command-line interface for interacting with the Inco Network testnet (Base Sepolia) to perform minting and shielding tasks, which may help qualify users for a potential Inco Network airdrop. It uses the Web3.py library to connect to the Base Sepolia testnet and manage transactions.

## About Inco Network Airdrop

Inco Network is a modular, interoperable Layer 1 blockchain focused on confidentiality for decentralized applications. Participating in testnet activities, such as minting and shielding test tokens on the Base Sepolia testnet, may qualify users for a potential airdrop of Inco's native tokens. For more details, check the official Inco Network website, Discord, or Twitter for updates on eligibility and snapshot dates.

## Prerequisites

- **Python**: Version 3.8 or higher

## Installation

Follow these steps to set up the script for the Inco Network airdrop:

1. **Clone the Repository**  
   Clone this repository to your local machine:
   ```bash
   git clone https://github.com/Aguh18/Inco_Network_Auto_Mint_Shield_Bot.git
   cd Inco_Network_Auto_Mint_Shield_Bot
   ```

2. **Create a Virtual Environment** (Recommended)  
   Set up a Python virtual environment to manage dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**  
   Install the required Python packages listed in `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
  

4. **Set Up Environment Variables**  
   Create a `.env` file in the project root directory using a text editor (e.g., Notepad on Windows, VS Code, or any code editor). Add the following line to the file:
   ```
   PRIVATE_KEY=your_private_key_here
   ```
   Replace `your_private_key_here` with your wallet's private key (without the `0x` prefix). Save the file as `.env`. Never share your private key.


6. **Run the Script**  
   Execute the script to start interacting with the testnet:
   ```bash
   python main.py
   ```



## Notes

- **Testnet Safety**: The script uses test tokens, so no real funds are at risk. Secure your private key.
- **Gas Fees**: Ensure your wallet has sufficient test ETH for transaction fees.
- **Airdrop Eligibility**: Inco Network has not officially confirmed an airdrop, but consistent testnet participation is recommended. Check official channels for updates.
- **Interrupt**: Press `Ctrl+C` to exit the script gracefully.

## Disclaimer
For Education only. Use at your own risk. Creators aren’t liable for issues.

## License
MIT License

## Community

- [AutoDropz Telegram](https://t.me/+V_JQTTMVZVU3YTM9)