import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from PIL import Image

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# The Load_Contract Function
################################################################################

@st.cache(allow_output_mutation=True)
def load_contract():

    # Load the contract ABI
    with open(Path('./contracts/compiled/TeamTokens_abi.json')) as f:
        TeamTokens_abi = json.load(f)

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
st.image(image)
st.header("Welcome to Team Tokens")
st.write ("Fans buy and cheer on their favorite NCAA team during the March Madness Tournament")



################################################################################
# Make New Bet
################################################################################

st.title("Make Bet")
accounts = w3.eth.accounts
team = {"Kansas":0, "Brooklyn Nets":1, "New York Knicks": 2, "Philadelphia 76ers": 3, "Toronto Raptors":4}
# Use a Streamlit component to get the address of the wallet
address = st.selectbox("Account", options=accounts)

# Use a Streamlit component to get the artwork's URI
st.text("Each token is 0.05 Ether and the gas is 0.01 Ether")
amount = int(st.number_input("How much token do you want to purchase?"))
id_team = int(st.number_input("Team"))
#id_team = int(st.selectbox("Team", options=team))


if st.button("Bet"):

    # Use the contract to send a transaction to the mint function
    tx_hash = contract.functions.mint(
        address,
        id_team,
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
teams = int(st.number_input("ID"))
tokens = contract.functions.balanceOf(selected_address,teams).call()

st.write(f"This address owns {tokens} tokens")

################################################################################
# Side bar for the Total Team supply
################################################################################
st.sidebar.markdown("## Total Tokens per Team")

for i in range(64):
    totaltokens = contract.functions.totalSupply(i).call()
    st.sidebar.write(f"Team {i+1} has {totaltokens} tokens")


