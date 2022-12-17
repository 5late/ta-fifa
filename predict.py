import json
import os
import cmds
import smart


# Personal winrate
def calculateWinrate():
    name, ta, grade = cmds.getName().split('-')

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

    first_move_winrate = (games_moved_won / games_moved) * 100

    return first_move_winrate

def opponentWinRate():
    opp_name, opp_ta, opp_grade = cmds.getName('Enter Opponent Name: ').split('-')

    opp_winrate = smart.getPersonalWinRate(opp_name, opp_ta, opp_grade)

    return opp_winrate

def calculateWinrateWeightSecond(winrate, opp_winrate):
    if winrate - opp_winrate >= 0:
        winrate_weight = ((0.65 * ((winrate - opp_winrate)**2))/100)+35
        opp_winrate_weight = 65 - winrate_weight
    elif winrate - opp_winrate < 0:
        winrate_weight = -(((0.65 * ((opp_winrate - winrate) ** 2))/100)+35) + 70
        opp_winrate_weight = 65 + ((0.65 * ((opp_winrate - winrate)**2))/100) + 35 - 70
    
    return winrate_weight/100, opp_winrate_weight/100

def calculateWinrateWeightFirst(winrate, opp_winrate):
    if winrate - opp_winrate >= 0:
        winrate_weight = ((0.55 * ((winrate - opp_winrate)**2))/100)+32.5
        opp_winrate_weight = 55 - winrate_weight
    elif winrate - opp_winrate < 0:
        winrate_weight = -(((0.55 * (-(winrate - opp_winrate) ** 2))/100)+32.5) + 65
        opp_winrate_weight = 55 + ((0.55 * (-(winrate - opp_winrate)**2))/100) - 65
    
    return winrate_weight/100, opp_winrate_weight/100
    
def calculateOdds():
    name, ta, grade, winrate = calculateWinrate()
    opp_winrate = opponentWinRate()
    first_mover_winrate, second_mover_winrate = calculateFirstMoverWinRate(name, ta)

    first_mover_winrate_weight = 0.2
    second_mover_winrate_weight = 0.25
    first_move_winrate_weight = 0.25

    first_mover = input('Who is moving first?: ').lower()
    first_move = input('What was the first move?: ').lower()

    if first_mover == name:
        winrate_weight, opp_winrate_weight = calculateWinrateWeightFirst(winrate, opp_winrate)
        first_move_winrate = calculateFirstMoveWinRate(name, ta, first_move)

        odds = (winrate * winrate_weight) - (opp_winrate * opp_winrate_weight) + (first_mover_winrate * first_mover_winrate_weight) + (first_move_winrate * first_move_winrate_weight)
    else:
        winrate_weight, opp_winrate_weight = calculateWinrateWeightSecond(winrate, opp_winrate)
        second_mover_winrate_weight = 0.35
        odds = (winrate * winrate_weight) - (opp_winrate * opp_winrate_weight) + (second_mover_winrate * second_mover_winrate_weight)

    print(winrate_weight, opp_winrate_weight, second_mover_winrate)
    print(f'{name} has {round(odds, 2)}% of winning.')
