# TODO: CONSOLIDATE BETS WITH FUNCTION TO ACTUALLY PAYOUT A BET
import json
import cmds
import predict
from datetime import datetime
import time
import os

def mainMenu():
    print('1. Check Balance')
    print('2. Check Outstanding Bets')
    print('3. Create New Bet')
    print('4. Edit a Bet')
    print('5. Remove a Bet')
    print('6. Consolidate Bets')

    choice = input('Enter your selection: ')

    if choice == '1':
        printBalance()
    elif choice == '2':
        printOutstandingBets()
    elif choice == '3':
        createBet()
    elif choice == '5':
        removeBet()
    elif choice == '6':
        consolidateBets()


def printBalance():
    balance = checkBalance()
    print('Your balance is: $$' + str(balance))

def checkBalance(name='', ta=''):
    consolidateBets()
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
    consolidateBets()
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

    return bet_amount_pre_tax + total_fees, total_fees

def bigBrothersWallet(name, ta, transaction_type, amount):
    with open('data/players/01-BIGBROTHER.json', 'r') as file:
        data = json.load(file)

        if transaction_type == 'in':
            data['balance'] += amount
            data['transactions'].append(f'IN-{amount}-{name}-{ta}')
        elif transaction_type == 'out':
            data['balance'] -= amount
            data['transactions'].append(f'OUT-{amount}-{name}-{ta}')
        
        data['last_interaction'] = f'{name}-{ta}'

    outfile = json.dumps(data, indent=4)

    with open(f'data/players/01-BIGBROTHER.json', 'w') as f:
        f.write(outfile)

def createBet(name='', ta=''):
    consolidateBets()
    if len(name) == 0:
        name, ta, grade = cmds.getName('Enter Name [Ryan/Christian]: ').split('-')

    player_one, player_one_ta, player_one_grade, player_one_winrate = predict.calculateWinrate(msg='Enter Player 1: ')
    player_two, player_two_ta, player_two_grade, player_two_winrate = predict.calculateWinrate(msg='Enter Player 2: ')

    bet_amount = int(input('Enter the bet amount: '))

    bet_amount_post_tax, fees = convertFees(bet_amount)

    balance = checkBalance(name, ta)

    while bet_amount_post_tax > balance:
        print('You do not have that much money.')
        bet_amount = int(input('Enter the bet amount: '))
        bet_amount_post_tax, fees = convertFees(bet_amount)

    bigBrothersWallet(name, ta, 'in', bet_amount_post_tax) # take the money with taxes and fees

    bet_on = input('Who would you like to bet on?: ')
    while bet_on != player_one and bet_on != player_two:
        print('You have to bet on one of the players you entered.')
        bet_on = input('Who would you like to bet on?: ')

    ticks = int(time.time())
    id = generateBetId(name, ta, player_one, player_one_ta, player_two, player_two_ta, str(bet_amount), str(ticks))

    date = datetime.now().strftime("%d/%m/%Y")

    oname, opp_name, decimal_odds, decimal_opp_odds, implied_odds, implied_opp_odds = predict.calculateMultipleMatches(player_one, player_one_ta, player_one_grade, player_one_winrate, player_two, player_two_ta, player_two_grade, player_two_winrate, 'd', 2)

    if bet_on == oname:
        odds = decimal_odds
    elif bet_on == opp_name:
        odds = decimal_opp_odds

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
            "bet_on":bet_on,
            "bet_amount": bet_amount,
            "bet_odds": odds
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

        bet_data['bets']['balance'] = bet_data['bets']['balance'] - bet_amount_post_tax
        bets.append(id)

    bet_outfile = json.dumps(bet_data, indent=4)

    with open(f'data/players/{name}-{ta}.json', 'w') as f:
        f.write(bet_outfile)
    
    print(f'New Bet Created with ID: {id}')

def removeBet(name='', ta=''):
    consolidateBets()
    if len(name) == 0:
        name, ta, grade = cmds.getName('Enter Name [Ryan/Christian]: ').split('-')

    bets = checkOutstandingBets(name, ta)

    print('You have the following outstanding bets: ' + str(bets))

    print('Fill out the following details about the bet you want to cancel.')

    player_one, player_one_ta, player_one_grade = cmds.getName('Enter Player 1: ').split('-')
    player_two, player_two_ta, player_two_grade = cmds.getName('Enter Player 2: ').split('-')

    bet_amount = 0
    ticks = 0

    remove_id = generateBetId(name, ta, player_one, player_one_ta, player_two, player_two_ta, str(bet_amount), str(ticks))

    for bet in bets:
        if bet.split('-')[0].split('_V_')[0].split('_')[0] == player_one and bet.split('-')[0].split('_V_')[0].split('_')[1] == player_one_ta:
            if bet.split('-')[0].split('_V_')[1].split('_')[0] == player_two and bet.split('-')[0].split('_V_')[1].split('_')[1] == player_two_ta:
                with open(f'data/bets/{bet}.json', 'r') as bet_file:
                    data = json.load(bet_file)

                    data['meta']['status'] = 'CLOSED'
                
                with open(f'data/players/{name}-{ta}.json', 'r') as player_file:
                    player_data = json.load(player_file)

                    outstanding_bets = player_data['bets']['outstanding_bets']

                    outstanding_bets.remove(bet)
                    player_data['bets']['balance'] += round(data['bet_info']['bet_amount'] * 1.13)

                    bigBrothersWallet(name, ta, 'out', data['bet_info']['bet_amount'] * 1.13) # refund taxes but not fees

                bet_outfile = json.dumps(data, indent=4)

                with open(f'data/bets/{bet}.json', 'w') as f:
                    f.write(bet_outfile)

                player_outfile = json.dumps(player_data, indent=4)

                with open(f'data/players/{name}-{ta}.json', 'w') as player_f:
                    player_f.write(player_outfile)
            
                print('Removed bet: ' + str(bet))

def consolidateBets():
    all_bets_path = 'data/bets/'

    for bet in os.listdir(all_bets_path):
        bet = bet.removesuffix('.json')
        won = 0
        lost = 0
        with open(f'data/bets/{bet}.json', 'r') as file:
            data = json.load(file)

            if data['meta']['status'] == 'OUTSTANDING':
                player_one = data['players']['player_one']['name']
                player_two = data['players']['player_two']['name']

                player_one_ta = data['players']['player_one']['ta']
                player_two_ta = data['players']['player_two']['ta']
                
                played = cmds.getCheckMatchup(player_one, player_two, player_one_ta, player_two_ta)

                if not played:
                    continue
                else:
                    with open(f'data/games/{played}.json', 'r') as game_file:
                        game_data = json.load(game_file)

                        outcome = game_data['outcome']['outcome_word']

                        if outcome == 'win':
                            if game_data['outcome']['winner']['name'] == data['bet_info']['bet_on']:
                                won += 1
                            else:
                                lost += 1
                        
                        following_games = game_data['meta']['following_games']
                        
                        if len(following_games) > 0:
                            for follow_game in following_games:
                                with open(f'data/games/{follow_game}.json', 'r') as follow_game_file:
                                    follow_data = json.load(follow_game_file)

                                    outcome = follow_data['outcome']['outcome_word']

                                    if outcome == 'win':
                                        if follow_data['outcome']['winner']['name'] == data['bet_info']['bet_on']:
                                            won += 1
                                        else:
                                            lost += 1
                
                    if won > lost:
                        data['meta']['status'] = 'WON'
                        win_amount = data['bet_info']['bet_amount'] * data['bet_info']['bet_odds']

                        better = data['bet_info']['better_name']
                        better_ta = data['bet_info']['better_ta']

                        bigBrothersWallet(better, better_ta, 'out', win_amount)

                        with open(f'data/players/{better}-{better_ta}.json', 'r') as player_file:
                            player_data = json.load(player_file)

                            player_data['bets']['balance'] += win_amount
                            player_data['bets']['outstanding_bets'].remove(bet)
                    
                        player_outfile = json.dumps(player_data, indent=4)

                        with open(f'data/players/{better}-{better_ta}.json', 'w') as player_f:
                            player_f.write(player_outfile)

                    elif won <= lost:
                        data['meta']['status'] = 'LOST'

                        better = data['bet_info']['better_name']
                        better_ta = data['bet_info']['better_ta']

                        with open(f'data/players/{better}-{better_ta}.json', 'r') as player_file:
                            player_data = json.load(player_file)
                            player_data['bets']['outstanding_bets'].remove(bet)
                    
                        player_outfile = json.dumps(player_data, indent=4)

                        with open(f'data/players/{better}-{better_ta}.json', 'w') as player_f:
                            player_f.write(player_outfile)
                    
                    bet_outfile = json.dumps(data, indent=4)

                    with open(f'data/bets/{bet}.json', 'w') as bet_f:
                        bet_f.write(bet_outfile)
        
                print(f'Consolidated bet {bet}.')
