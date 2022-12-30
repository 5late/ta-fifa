import json
import os
import cmds
import smart


# Personal winrate
def calculateWinrate(name='', ta='', grade='', msg='Enter Name: '):
    if len(name) == 0:
        name, ta, grade = cmds.getName(msg).split('-')

    winrate = smart.getPersonalWinRate(name, ta, grade)

    return name, ta, grade, winrate

# First Mover Win Rate
def calculateFirstMoverWinRate(name, ta):
    with open(f'data/players/{name}-{ta}.json', 'r') as file:
        data = json.load(file)

        games_played = data['games_played']

        games_moved_first = 0
        games_moved_first_won = 0

        games_moved_second = 0
        games_moved_second_won = 0

        for game in games_played:
            with open(f'data/games/{game}.json', 'r') as game_file:
                game_data = json.load(game_file)

                if game_data['first_mover'] == name:
                    games_moved_first += 1
                    if game_data['outcome']['winner']['name'] == name:
                        games_moved_first_won += 1
                else:
                    games_moved_second += 1
                    if game_data['outcome']['winner']['name'] == name:
                        games_moved_second_won += 1

        if games_moved_first == 0:
            games_moved_first = 1
        if games_moved_second == 0:
            games_moved_second = 1

        first_move_winrate = (games_moved_first_won / games_moved_first) * 100
        second_move_winrate = (games_moved_second_won / games_moved_second) * 100

    return first_move_winrate, second_move_winrate

def calculateFirstMoveWinRate(name, ta, move):
    with open(f'data/players/{name}-{ta}.json', 'r') as file:
        data = json.load(file)

        games_played = data['games_played']

        games_moved = 0
        games_moved_won = 0

        for game in games_played:
            with open(f'data/games/{game}.json', 'r') as game_file:
                game_data = json.load(game_file)

                if game_data['first_mover'] == name:
                    if game_data['first_move'] == move:
                        games_moved += 1
                        if game_data['outcome']['winner']['name'] == name:
                            games_moved_won += 1

    if games_moved == 0:
        games_moved = 1
    first_move_winrate = (games_moved_won / games_moved) * 100

    return first_move_winrate

def opponentWinRate(opp_name='', opp_ta='', opp_grade=''):
    if len(opp_name) == 0:
        opp_name, opp_ta, opp_grade = cmds.getName('Enter Opponent Name: ').split('-')

    opp_winrate = smart.getPersonalWinRate(opp_name, opp_ta, opp_grade)

    return opp_name, opp_ta, opp_grade, opp_winrate

def checkForPrevGame(name, ta, opp_name, opp_ta):
    with open(f'data/players/{name}-{ta}.json', 'r') as file:
        data = json.load(file)

        games_played = data['games_played']

        for game in games_played:
            with open(f'data/games/{game}.json', 'r') as game_file:
                game_data = json.load(game_file)
                if game_data['players']['player_one']['name'] == opp_name and game_data['players']['player_one']['ta'] == opp_ta:
                    return game
                elif game_data['players']['player_two']['name'] == opp_name and game_data['players']['player_two']['ta'] == opp_ta:
                    return game
        
    return False

def getPrevGameWeight(name, game):
    with open(f'data/games/{game}.json', 'r') as game_file:
        game_data = json.load(game_file)

        winner = game_data['outcome']['winner']['name']
        prev_games = game_data['meta']['previous_games']
        follow_games = game_data['meta']['following_games']

        games_won = 0
        games_played = 0

        if len(prev_games) > 0:
            for prev_game in prev_games:
                games_played += 1
                with open(f'data/games/{prev_game}.json', 'r') as prev_game_file:
                    prev_game_data = json.load(prev_game_file)

                    prev_winner = prev_game_data['outcome']['winner']['name']

                    if prev_winner == name:
                        games_won += 1
        
        if len(follow_games) > 0:
            for follow_game in follow_games:
                games_played += 1
                with open(f'data/games/{follow_game}.json', 'r') as follow_game_file:
                    follow_game_data = json.load(follow_game_file)

                    follow_winner = follow_game_data['outcome']['winner']['name']

                    if follow_winner == name:
                        games_won += 1

        game_winrate = (games_won / games_played) * 100
        game_winrate_weight = 0.25

        return game_winrate * game_winrate_weight

def calculateWinrateWeightSecond(winrate, opp_winrate):
    if winrate - opp_winrate >= 0:
        winrate_weight = ((0.65 * ((winrate - opp_winrate)**2))/100)+35
        opp_winrate_weight = 65 - winrate_weight
    elif winrate - opp_winrate < 0:
        winrate_weight = -(((0.65 * ((opp_winrate - winrate) ** 2))/100)+35) + 70
        opp_winrate_weight = 65 + ((0.65 * ((opp_winrate - winrate)**2))/100) + 35 - 70
    
    if winrate_weight > 65:
        winrate_weight = 60
        opp_winrate_weight = 5
    elif opp_winrate_weight > 65:
        winrate_weight = 5
        opp_winrate_weight = 60
    
    return winrate_weight/100, opp_winrate_weight/100

def calculateWinrateWeightFirst(winrate, opp_winrate):
    if winrate - opp_winrate >= 0:
        winrate_weight = ((0.55 * ((winrate - opp_winrate)**2))/100)+32.5
        opp_winrate_weight = 55 - winrate_weight
    elif winrate - opp_winrate < 0:
        winrate_weight = -(((0.55 * ((winrate - opp_winrate) ** 2))/100)+32.5) + 65
        opp_winrate_weight = 55 + ((0.55 * ((opp_winrate - winrate)**2))/100) + 32.5 - 65
    
    if winrate_weight > 55:
        winrate_weight = 50
        opp_winrate_weight = 5
    elif opp_winrate_weight > 55:
        winrate_weight = 5
        opp_winrate_weight = 50
    
    return winrate_weight/100, opp_winrate_weight/100
    
def calculateConsistency(name, ta):
    with open(f'data/players/{name}-{ta}.json', 'r') as f:
        data = json.load(f)

        games_played = data['games_played']

        matchups = 0
        consistent_matchups = 0 # matchups where player won both matches

        for game in games_played:
            matchups += 1
            won = 0
            with open(f'data/games/{game}.json', 'r') as game_file:
                game_data = json.load(game_file)

                if game_data['outcome']['winner']['name'] == name:
                    won += 1

                following_games = game_data['meta']['following_games']

                if len(following_games) > 0:
                    for follow_game in following_games:
                        with open(f'data/games/{follow_game}.json', 'r') as follow_game_file:
                            follow_game_data = json.load(follow_game_file)

                            if follow_game_data['outcome']['winner']['name'] == name:
                                won += 1
                
            if won >= 2:
                consistent_matchups += 1
    
    return round((consistent_matchups/(matchups/2)) * 100, 2)

                

def calculateOdds(name='', ta='', grade='', winrate=0, opp_name='', opp_ta='', opp_grade='', opp_winrate=0, first_mover='', first_move='', multiple_match=False, matches=0):
    ran_before = False
    if len(name) == 0:
        name, ta, grade, winrate = calculateWinrate()
        opp_name, opp_ta, opp_grade, opp_winrate = opponentWinRate()
        first_mover = input('Who is moving first?: ').lower()
        first_move = input('What was the first move?: ').lower()
    else:
        if not multiple_match:
            ran_before = True
    first_mover_winrate, second_mover_winrate = calculateFirstMoverWinRate(name, ta)

    played_before = checkForPrevGame(name, ta, opp_name, opp_ta)

    if not played_before:
        first_mover_winrate_weight = 0.2
        second_mover_winrate_weight = 0.25
        first_move_winrate_weight = 0.25
    else:
        first_mover_winrate_weight = 0.1
        second_mover_winrate_weight = 0.1
        first_move_winrate_weight = 0.1
        prev_game = getPrevGameWeight(name, played_before)

    if first_mover == name:
        winrate_weight, opp_winrate_weight = calculateWinrateWeightFirst(winrate, opp_winrate)
        first_move_winrate = calculateFirstMoveWinRate(name, ta, first_move)

        if not played_before:
            odds = (winrate * winrate_weight) - (opp_winrate * opp_winrate_weight) + (first_mover_winrate * first_mover_winrate_weight) + (first_move_winrate * first_move_winrate_weight)
        else:
            odds = (winrate * winrate_weight) - (opp_winrate * opp_winrate_weight) + (first_mover_winrate * first_mover_winrate_weight) + (first_move_winrate * first_move_winrate_weight) + prev_game
    else:
        winrate_weight, opp_winrate_weight = calculateWinrateWeightSecond(winrate, opp_winrate)

        if not played_before:
            second_mover_winrate_weight = 0.35
            odds = (winrate * winrate_weight) - (opp_winrate * opp_winrate_weight) + (second_mover_winrate * second_mover_winrate_weight)
        else:
            odds = (winrate * winrate_weight) - (opp_winrate * opp_winrate_weight) + (second_mover_winrate * second_mover_winrate_weight) + prev_game

    #print(winrate_weight, opp_winrate_weight, first_mover_winrate, prev_game)
    if odds < 0:
        odds = 0
    luck = 7
    if odds < 90:
        odds = odds + luck
    if not ran_before and not multiple_match:
        calculateOdds(opp_name, opp_ta, opp_grade, opp_winrate, name, ta, grade, winrate, first_mover, first_move)
    if multiple_match:
        consistency = calculateConsistency(name, ta)
        odds = (1.00 - (matches * 0.0125)) * odds + (matches * 0.0125) * consistency
        return name, odds
    print(f'{name} has {round(odds, 2)}% of winning.')


def calculateMultipleMatches(name='', ta='', grade='', winrate=0, opp_name='', opp_ta='', opp_grade='', opp_winrate=0, first_move='', matches=''):
    if len(name) == 0:
        name, ta, grade, winrate = calculateWinrate()
        opp_name, opp_ta, opp_grade, opp_winrate = opponentWinRate()

    total = 0
    total_opp = 0

    for i in range(matches):
        if i % 2 == 0:
            first_mover = name
            func_name, odds = calculateOdds(name, ta, grade, winrate, opp_name, opp_ta, opp_grade, opp_winrate, first_mover, first_move, True, matches)
            total += odds
        else:
            first_mover = opp_name
            func_name, odds = calculateOdds(name, ta, grade, winrate, opp_name, opp_ta, opp_grade, opp_winrate, first_mover, first_move, True, matches)
            total += odds
        
    for i in range(matches):
        if i % 2 == 0:
            first_mover = name
            func_name, odds = calculateOdds(opp_name, opp_ta, opp_grade, opp_winrate, name, ta, grade, winrate, first_mover, first_move, True, matches)
            total_opp += odds
        else:
            first_mover = opp_name
            func_name, odds = calculateOdds(opp_name, opp_ta, opp_grade, opp_winrate, name, ta, grade, winrate, first_mover, first_move, True, matches)
            total_opp += odds
    
    total_odds = round(total / matches, 2) # these are fractional odds
    total_opp_odds = round(total_opp / matches, 2)

    decimal_odds = round(total_opp_odds/total_odds, 2) + 1 # these are decimal odds
    decimal_opp_odds = round(total_odds/total_opp_odds, 2) + 1

    implied_odds = round(1/decimal_odds, 2) * 100
    implied_opp_odds = round(1/decimal_opp_odds, 2) * 100

    return name, opp_name, decimal_odds, decimal_opp_odds, implied_odds, implied_opp_odds

def printMultipleMatches():
    first_move = input('What should the first move be?: ').lower()
    matches = int(input('How many matches are going to be played?: '))

    name, opp_name, decimal_odds, decimal_opp_odds, implied_odds, implied_opp_odds = calculateMultipleMatches(first_move=first_move, matches=matches)
    print(f'{name} has {implied_odds}% of winning. Betting Odds: {decimal_odds}.')
    print(f'{opp_name} has {implied_opp_odds}% of winning. Betting Odds: {decimal_opp_odds}.')
