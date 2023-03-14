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
team = {"Alabama Crimson Tide":0, "Houston Cougars":1, "Kansas Jayhawks": 2, "Purdue Boilermakers": 3, "Arizona Wildcats":4,
"Texas Longhorns": 5, "UCLA Bruins":6, "Marquette Golden Eagles":7, "Baylor Bears":8, "Xavier Musketeers":9,
"Gonzaga Bulldogs":10, "Kansas State Wildcats":11, "Virginia Cavaliers": 12, "Indiana Hoosiers":13, "UConn Huskies":14, "Tennessee Volunteers":15,
"San Diego State Aztecs":16, "Miami Hurricanes":17, "Saint Mary's Gaels":18, "Duke Blue Devils":19, "Creighton Bluejays":20, "Iowa State Cyclones":21,
"TCU Horned Frogs":22, "Kentucky Wildcats":23, "Missouri Tigers":24, "Texas A&M Aggies":25, "Northwestern Wildcats":26, "Michigan State Spartans":27,
"Maryland Terrapins":28,"Iowa Hawkeyes" :29, "Arkansas Razorbacks":30, "Memphis Tigers":31, "West Virginia Mountaineers":32,
"Auburn Tigers":33, "Illinois Fighting Illini":34, "Florida Atlantic Owls":35, "Utah State Aggies":36, "Penn State Nittany Lions" :37,
"Boise State Broncos":38, "USC Trojans":39, "NC State Wolfpack":40, "Mississippi State Bulldogs":41,
"Pittsburgh Panthers":42, "Arizona State Sun Devils":43, "Nevada Wolf Pack":44, "Providence Friars":45, 
"Charleston Cougars":46, "Drake Bulldogs":47, "VCU Rams":48, "Oral Roberts Golden Eagles":49, "Furman Paladins":50,
"Kent State Golden Flashes":51, "Iona Gaels":52, "Louisiana Ragin' Cajuns":53, "UC Santa Barbara Gauchos":54, 
"Kennesaw State Owls":55, "Grand Canyon Lopes":56, "Montana State Bobcats":57, "Princeton Tigers":58, 
"Colgate Raiders":59, "UNC Asheville Bulldogs" :60, "Vermont Catamounts":61, "Texas A&M-Corpus Christi Islanders":62, 
"Southeast Missouri State Redhawks":63, "Northern Kentucky Norse":64, "Howard Bison":65, 
"Texas Southern Tigers":66, "Fairleigh Dickinson Knights":67}

trans_fee = 1000000000000000 #0.001 Ether
token_cost = 5000000000000000 #0.005 Ether
# Use a Streamlit component to get the address of the wallet
address = st.selectbox("Account", options=accounts)


# Use a Streamlit component to make a bet
amount = st.number_input("1 token costs 0.005 Ether. How many tokens do you want to purchase?", value = 0)
value_cost = amount * token_cost + trans_fee

#id_team = st.number_input("Team", value = 0)
id_team = st.selectbox("Choose Your Favorite Team:", options=team, kwargs=team)


if st.button("Bet"):
    # Use the contract to send a transaction to the mint function
    tx_hash = contract.functions.mint(
        address,
        team[id_team],
        amount
    ).transact({'from': address,'value': value_cost, 'gas': 100000})

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

#Print number of tokens
st.write(f"This address owns {round(tokens,2)} tokens")


################################################################################
# Side bar for the Total Team supply
################################################################################
st.sidebar.markdown("## Total Bet(Tokens) per Team")
pool_token = 0

# call contract_balance
contract_balance = contract.functions.getContractBalance().call()

# loop through team dictionary and get the total tokens
for i,j in team.items():
    #Call contract function totalSupply
    totaltokens = contract.functions.totalSupply(j).call()
    pool_token += totaltokens

# loop through team dictionary and print out the total token per team
for i,j in team.items():
    #Call contract function totalSupply
    totaltokens = contract.functions.totalSupply(j).call()
    
    if totaltokens > 0:
        #print Team and Tokens
        st.sidebar.write(f"{i}: {round(totaltokens,2)} tokens")
        st.sidebar.write(f"Odds = {round(pool_token/totaltokens,0)} : 1")

    

# Write the total tokens
st.sidebar.write(f"Total Tokens: {pool_token}")


# Retreive contract balance
contract_balance = contract.functions.getContractBalance().call()
contract_balance = contract_balance/1000000000000000000  # 1 ether  = 1000000000000000000
st.sidebar.write(f"Contract Balance: {contract_balance} Ether")