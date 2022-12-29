import json
import cmds
from datetime import datetime

def mainMenu():
    print('1. Check Balance')
    print('2. Check Outstanding Bets')
    print('3. Create New Bet')
    print('4. Edit a Bet')
    print('5. Remove a Bet')

    choice = input('Enter your selection: ')

    if choice == '1':
        printBalance()


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

def generateBetId(name, ta, player_one, player_one_ta, player_two, player_two_ta, bet_amount):
    id = player_one.lower() + "_" + player_one_ta.lower() + "_V_" + player_two.lower() + "_" + player_two_ta.lower() + "-" + bet_amount.lower() + "-" + name.lower() + "_" + ta.lower()

    return id

def createBet(name='', ta=''):
    if len(name) == 0:
        name, ta, grade = cmds.getName('Enter Name [Ryan/Christian]: ').split('-')

    player_one, player_one_ta, player_one_grade = cmds.getName('Enter Player 1: ').split('-')
    player_two, player_two_ta, player_two_grade = cmds.getName('Enter Player 2: ').split('-')

    bet_amount = int(input('Enter the bet amount: '))

    balance = checkBalance()

    while bet_amount > balance:
        print('You do not have that much money.')
        bet_amount = int(input('Enter the bet amount: '))

    id = generateBetId(name, ta, player_one, player_one_ta, player_two, player_two_ta, str(bet_amount))

    ticks = (datetime.utcnow() - datetime(1,1,1)).total_seconds()
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

    

