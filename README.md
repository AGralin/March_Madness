# March Madness
![Image](./Images/marchmadness_logo_ncaa.gif)
## Team Members: Adam, Faith, Wade and Yen
---

## Project Overview:

- March Madness betting game using smart contracts.
- Each of the 64 NCAA teams has their own ERC-1155 token (these tokens are semi-fungible, which allows multiple NFTs to be minted with the same id).
- There is a public mint function that allows anyone to mint as many tokens as they want for any team.
- The funds from the mint go directly into the prize pool.
    - This means that the odds change every time someone mints.
- At the end of March Madness, only the people that own the winning team tokens will be paid. 
    - Payout = (prize pool / total supply of winners tokens minted) * amount of winners tokens owned
- Created a simple UI using Streamlit where you can mint and view your balance of each token.
---
## Detailed Usage and installation instructions:

- **Requirements:**
    - Ganache (private Ethereum blockchain environment)
    - Metamask with at least two wallets imported from Ganache
    - Remix IDE: https://remix.ethereum.org/
    - Visual Studio Code
    - Terminal/GitBash with Streamlit installed in dev environment
    - Copy of this repository on your local computer
    

- **Instructions:**
    - Start Ganache and open a workspace
    - Go to remix.ethereum.org in your preferred browser and create a file that ends in ".sol"
    - Copy the contents of the TeamTokens.sol file and paste it into the solidity file you created in remix
    - Compile your solidity file
    - Go to "DEPLOY & RUN TRANSACTIONS" and select Metamask in the Environment dropdown
    - Deploy the contract and confirm the transaction in Metamask
    - Once your contract is deployed, copy the contract address and paste it into the .env file where it says "SMART_CONTRACT_ADDRESS"
    - In remix, go to "SOLIDITY COMPILER" and copy the ABI
    - In Visual Studio Code, open the "TeamTokens_abi.json" file and paste the ABI you copied from remix
    - Ensure that you saved the changes made to the .env and .json files
    - Open Terminal/GitBash and cd into the correct folder
    - Activate dev environment and type "streamlit run app.py" (this should open the interface in your browser automatically)
--- 

## Data Collection and Preparation:

- **OpenZeppelin Github:**
    - https://github.com/OpenZeppelin/openzeppelin-contracts/tree/master/contracts/token/ERC1155
- **Contracts Wizard (template for creating smart contracts):**
    - https://docs.openzeppelin.com/contracts/4.x/wizard

- **NCAA Website:**
    -https://www.ncaa.com/scoreboard/basketball-men/d1

Examples of the application or results:

Summary of the analysis/Next Steps: 
- Address the following questions: Does an oracle make a smart contract more trustworthy to players? Or more vulnerable to hacks and people would prefer the contract owner distribute winnings?
- Add metadata using Ipfs
- Research the legality - both for sports betting and crypto. Need legal opinions.
- Launch DApp

Note: Video of app? - Adam

---
Presentation: https://docs.google.com/presentation/d/1meHhTFnapBm_1EzukVolUBrP-xQTg6g2/edit?usp=share_link&ouid=112227308253472634696&rtpof=true&sd=true


