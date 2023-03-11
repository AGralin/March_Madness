import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
# Load the environment
load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# The Load_Contract Function
################################################################################

# Load the Contract
def load_contract():

    # Load the contract ABI
    with open(Path('./contracts/compiled/TeamTokens_abi.json')) as f:
        TeamTokens_abi = json.load(f)

    # Create the object using the smart contract address
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Load the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=TeamTokens_abi
    )

    return contract

contract = load_contract()


################################################################################
# Header
################################################################################
image = Image.open('./Images/marchmadness_logo_ncaa.gif')
st.image(image, width=300)
st.header("Welcome to Team Tokens")
st.write ("Where fans buy tokens and cheer for their favorite NCAA team during the March Madness Tournament")


################################################################################
# Place New Bet
################################################################################

st.subheader("Place a Bet")
accounts = w3.eth.accounts

# Identify the teams
team = {"Miami":0, "Virginia":1, "Duke": 2, "Marquette": 3, "UConn":4,
"Xavier": 5, "Creighton":6, "Indiana":7, "Purdue":8, "Michigan State":9,
"Iowa":10, "Northwestern":11, "Baylor": 12, "Kansas":13, "Texas":14, "Kansas State":15,
"Iowa State":16, "TCU":17, "Arizona":18, "UCLA":19, "Alabama":20, "Tennessee":21,
"Texas A&M":22, "Missouri":23, "Kentucky":24, "Houston":25, "Saint Mary's":26, "San Diego State":27}

# Use a Streamlit component to get the address of the wallet
address = st.selectbox("Account", options=accounts)
#address = st.text_input("Account")

# Use a Streamlit component to make a bet
amount = st.number_input("1 token costs 0.005 Ether. How many tokens do you want to purchase?", value = 0)

#id_team = st.number_input("Team", value = 0)
id_team = st.selectbox("Choose Your Favorite Team:", options=team, kwargs=team)


if st.button("Bet"):
    # Use the contract to send a transaction to the mint function
    tx_hash = contract.functions.mint(
        address,
        team[id_team],
        amount
    ).transact({'from': address, 'gas': 1000000})

    # Celebrate your successful bet placement
    st.balloons()

    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))

st.markdown("---")


################################################################################
# Display a Token
################################################################################
st.markdown("## Check Balance of an Account")

selected_address = st.selectbox("Select Account", options=accounts)
id_pick = st.selectbox("Team", key= 0, options=team, kwargs=team)

#Call function balanceOf in the contract
tokens = contract.functions.balanceOf(selected_address,team[id_pick]).call()

#Convert Wei to Eth, Eth to Token
eth1 = tokens/1000000000000000000
tok1 = eth1/0.005 

#Print number of tokens
st.write(f"This address owns {round(tok1,2)} tokens")

################################################################################
# Side bar for the Total Team supply
################################################################################
st.sidebar.markdown("## Total Bet(Tokens) per Team")
pool_token = 0
pool_eth = 0

# loop through team dictionary and print out the total token per team
for i,j in team.items():
    #Call contract function totalSupply
    totaltokens = contract.functions.totalSupply(j).call()
    #Convert Wei to Eth, Eth to Token
    eth = totaltokens/1000000000000000000
    tok = eth/0.005
    if tok > 0:
        #print Team and Tokens
        st.sidebar.write(f"{i}: {round(tok,2)} tokens")
    pool_token += tok
    pool_eth += eth

st.sidebar.write(f"Total Tokens: {pool_token}")
st.sidebar.write(f"Total Pool: {pool_eth} Ether")
