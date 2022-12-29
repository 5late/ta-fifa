import json
import cmds
from datetime import datetime
import time

def mainMenu():
    print('1. Check Balance')
    print('2. Check Outstanding Bets')
    print('3. Create New Bet')
    print('4. Edit a Bet')
    print('5. Remove a Bet')

    choice = input('Enter your selection: ')

    if choice == '1':
        printBalance()
    elif choice == '2':
        printOutstandingBets()
    elif choice == '3':
        createBet()


def printBalance():
    balance = checkBalance()
    print('Your balance is: $$' + str(balance))

def checkBalance(name='', ta=''):
    if len(name) == 0:
        name, ta, grade = cmds.getName('Enter Name [Ryan/Christian]: ').split('-')

    with open(f'data/players/{name}-{ta}.json', 'r') as file:
        data = json.load(file)

        balance = data['bets']['balance']
    
    return balance

def printOutstandingBets():
    bets = checkOutstandingBets()
    
    for bet in bets:
        bet_players = bet.split('-')[0]
        bet_amount = bet.split('-')[1]

        print(f'You have a bet placed on the game: {bet_players} for amount $${bet_amount}.')

def checkOutstandingBets(name='', ta=''):
    if len(name) == 0:
        name, ta, grade = cmds.getName('Enter Name: [Ryan/Christian]: ').split('-')

    with open(f'data/players/{name}-{ta}.json', 'r') as file:
        data = json.load(file)

        bets = data['bets']['outstanding_bets']
    
    return bets

def generateBetId(name, ta, player_one, player_one_ta, player_two, player_two_ta, bet_amount, ticks):
    id = player_one.lower() + "_" + player_one_ta.lower() + "_V_" + player_two.lower() + "_" + player_two_ta.lower() + "-" + bet_amount.lower() + "-" + name.lower() + "_" + ta.lower() + "-" + ticks

    return id

def convertFees(bet_amount_pre_tax):
    tax_amount = 0.13
    casino_fee = 0.01

    taxes = bet_amount_pre_tax * tax_amount
    casino_fees = bet_amount_pre_tax * casino_fee

    total_fees = taxes + casino_fees

    return bet_amount_pre_tax + total_fees
    

def createBet(name='', ta=''):
    if len(name) == 0:
        name, ta, grade = cmds.getName('Enter Name [Ryan/Christian]: ').split('-')

    player_one, player_one_ta, player_one_grade = cmds.getName('Enter Player 1: ').split('-')
    player_two, player_two_ta, player_two_grade = cmds.getName('Enter Player 2: ').split('-')

    bet_amount = int(input('Enter the bet amount: '))

    bet_amount_post_tax = convertFees(bet_amount)

    balance = checkBalance()

    while bet_amount_post_tax > balance:
        print('You do not have that much money.')
        bet_amount = int(input('Enter the bet amount: '))

    ticks = int(time.time())
    id = generateBetId(name, ta, player_one, player_one_ta, player_two, player_two_ta, str(bet_amount), str(ticks))

    date = datetime.now().strftime("%d/%m/%Y")

    data = {
        "meta":{
            "id": id,
            "date": date,
            "ticks": ticks,
            "status": 'OUTSTANDING',
        },
        "bet_info":{
            "better_name": name, 
            "better_ta": ta,
            "better_grade": grade,
            "bet_amount": bet_amount
        },
        "players":{
            "player_one":{
                "name": player_one,
                "ta": player_one_ta,
                "grade": player_one_grade
            },
            "player_two":{
                "name": player_two,
                "ta":player_two_ta,
                "grade": player_two_grade
            }
        }
    }

    outfile = json.dumps(data, indent=4)

    with open(f'data/bets/{id}.json', 'w') as f:
        f.write(outfile)


    with open(f'data/players/{name}-{ta}.json', 'r') as bet_file:
        bet_data = json.load(bet_file)

        bets = bet_data['bets']['outstanding_bets']
        balance = bet_data['bets']['balance']

        balance = balance - bet_amount_post_tax
        bets.append(id)

    bet_outfile = json.dumps(bet_data, indent=4)

    with open(f'data/players/{name}-{ta}.json', 'w') as f:
        f.write(bet_outfile)
    
    print(f'New Bet Created with ID: {id}')