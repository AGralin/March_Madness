# March Madness
![Image](./Images/marchmadness_logo_ncaa.gif)
## Team Members: Adam, Faith, Wade and Yen

**Project Overview:**
- March Madness betting game using smart contracts.
- Each of the 64 NCAA teams have their own ERC-1155 token (these tokens are semi-fungible, which allows multiple NFTs to be minted with the same id).
- There is a public mint function that allows anyone to mint as many tokens as they want for any team.
- The funds from the mint go directly into the prize pool.
    - This means that the odds change every time someone mints.
- At the end of March Madness, only the people that minted the winning teams tokens will be payed. 
    - payout = (amount of winners tokens owned / total supply of winners tokens minted) * prize pool
- Created a simple UI using Streamlit where you can mint and view your balance of each token.

Detailed Usage and installation instructions: 

Data Collection and Preparation:

Examples of the application or results:

Summary of the analysis: 

Note: Video of app?

Presentation: https://docs.google.com/presentation/d/1meHhTFnapBm_1EzukVolUBrP-xQTg6g2/edit?usp=share_link&ouid=112227308253472634696&rtpof=true&sd=true