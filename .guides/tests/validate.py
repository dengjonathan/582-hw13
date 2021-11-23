from web3 import Web3
import sys
from os import path
import random

w3 = Web3(Web3.EthereumTesterProvider())

# set pre-funded account as sender
sender_address = w3.eth.accounts[0]
userA = w3.eth.accounts[1]
userB = w3.eth.accounts[2]
w3.eth.default_account = sender_address

#print( f"{sender_address} : {w3.eth.get_balance(sender_address)}" )
#print( f"{userA} : {w3.eth.get_balance(userA)}" )
#print( f"{userB} : {w3.eth.get_balance(userB)}" )

from vyper import compile_code, compile_codes

def deployContract(contract_filename,args={}):
    with open(contract_filename,"r") as f:
        contract_source=f.read()

    contract_dict = compile_codes(contract_sources={contract_filename:contract_source},output_formats=["bytecode","abi"])
    CONTRACT = w3.eth.contract(abi=contract_dict[contract_filename]['abi'], bytecode=contract_dict[contract_filename]['bytecode'])

    # Submit the transaction that deploys the contract
    tx_hash = CONTRACT.constructor(**args).transact()

    # Wait for the transaction to be mined, and get the transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    CONTRACT = w3.eth.contract(abi=contract_dict[contract_filename]['abi'], address=tx_receipt.contractAddress )
    return CONTRACT

def validate(student_repo_path):
    try:
        DAO = deployContract("DAO.vy")
    except Exception as e:
        print( "Failed to deploy DAO contract!" )
        print( e )
        return 0

    try:
        Attacker = deployContract(f"{student_repo_path}/attacker.vy")
    except Exception as e:
        print( "Failed to deploy Attacker contract!" )
        print( e )
        return 0

    initial_dao_balance = random.randint(5,20)*10**10
    try:
        DAO.functions.deposit().transact({"from":userB,"to":DAO.address,"value":initial_dao_balance})
    except Exception as e:
        print( "Failed to send ETH to DAO contract" )
        print( "This is not your fault" )
        print( "Please contact the instructor" )
        print( e )
        return 0 

    initial_attacker_balance = w3.eth.get_balance(userA)
    deposit_amount = 10**10
    gas = 10**5*int( (w3.eth.get_balance(DAO.address)/deposit_amount))
    try:
        tx_hash = Attacker.functions.attack(dao_address=DAO.address).transact({"from":userA,"value": deposit_amount,"gas":gas})
    except Exception as e:
        print( f"Error: failed to run Attacker.functions.attack" )
        print( e )

    tx_info = w3.eth.get_transaction(tx_hash)
    tx_receipt = w3.eth.get_transaction_receipt(tx_hash)
    gas_cost = tx_receipt.gasUsed*tx_info.gasPrice

    final_attacker_balance = w3.eth.get_balance(userA)
    final_dao_balance = w3.eth.get_balance(DAO.address)
    max_profit = initial_dao_balance - gas_cost	
    profit = final_attacker_balance - initial_attacker_balance

    print( f"DAO's initial balance was: {initial_dao_balance}" )
    print( f"{deposit_amount} WEI was deposited through your contract" )
    print( f"You made {profit+gas_cost} WEI" )
    print( f"You paid {gas_cost} in gas fees" )

    if profit == max_profit:
        print( f"Success: you completely drained the DAO contract!" )
    else:
        if profit > 0:
            print( f"Error: the attack did not completely drain the DAO contract" )
        else:
            print( f"Error: your attack did not result in any profit!" )
        if w3.eth.get_balance(DAO.address) > deposit_amount:
            print( f"You could get more by recursing again" )
        if initial_attacker_balance + initial_dao_balance > final_attacker_balance + final_dao_balance + gas_cost:
            print( f"Error: your attack did not return all funds to the attacker" )	

    score = int( 100*(profit/max_profit) )

#	print( f"Estimated Gas = {gas}\nGas = {tx_info.gas}" )
#	print( f"Gas cost = {gas_cost}" )
#	print( f"attacker balance : {w3.eth.get_balance(userA)}" )
#	print( f"DAO balance : {w3.eth.get_balance(DAO.address)}" )
    return score