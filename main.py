import json
import os
import uuid
from datetime import datetime
import cmds
import smart
import predict
import bet

def main():
    print('What is happening')
    print('1 - New Game')
    print('2 - Edit Profile Grade')
    print('3 - TA Winrate')
    print('4 - Grade Winrate')
    print('5 - Personal Winrate')
    print('6 - Check If Match Has Happened')
    print('7 - Calculate odds of match winner (solo game)')
    print('8 - Calculate odds of matchup winner (multi game)')
    print('9 - Bet Main Menu')

    choice = input('Enter choice: ')

    if choice == '1':
        newGame()
    elif choice == '2':
        name = input('Enter name: ').lower()
        cmds.editProfileGrade(name)
    elif choice == '3':
        smart.taWinRate()
    elif choice == '4':
        smart.gradeWinRate()
    elif choice == '5':
        smart.personalWinRate()
    elif choice == '6':
        cmds.checkMatchup()
    elif choice == '7':
        predict.calculateOdds()
    elif choice == '8':
        predict.printMultipleMatches()
    elif choice == '9':
        bet.mainMenu()

def getPlayerInfo(name):
    with open('data/players.txt', 'r') as file:
        lines = file.readlines()

        possible = []

        for line in lines:
            if line.split('-')[0] == name:
                ta = line.split('-')[1].rstrip()
                grade = line.split('-')[2].rstrip()
                possible.append(f'{name}-{ta}-{grade}')
        
        if len(possible) > 1:
            print(possible)
            correct = input('Which TA: ')
            for possibility in possible:
                if possibility.split('-')[1] == correct:
                    ta = possibility.split('-')[1].rstrip()
                    grade = possibility.split('-')[2].rstrip()
        
        return ta, grade

def getChangelog(changelog, version):
    changes = []
    f = open(f'changelogs/{changelog}-changelog.txt')
    lines = f.readlines()

    for i in range(len(lines)):
        if lines[i].rstrip() == version:
            for line in lines[i:]:
                if line == '\n':
                    break
                changes.append(line.rstip())
    
    return changes

def addGameToProfileData(player, player_ta, id, winner, loser):
    date = datetime.now().strftime("%d/%m/%Y")
    f = open(f'data/players/{player}-{player_ta}.json')
    
    data = json.load(f)

    data['games_played'].append(id)
    data['last_played'] = date
    data['stats']['played'] += 1

    if winner == player:
        data['stats']['won'] += 1
    elif loser == player:
        data['stats']['lost'] += 1
    else:
        data['stats']['draws'] += 1

    f.close()
    
    
    with open(f'data/players/{player}-{player_ta}.json', 'w') as file:
        outfile = json.dumps(data, indent=4)
        file.write(outfile)

def addGameToProfile(player_one, player_one_ta, player_two, player_two_ta, id, winner, loser):
    addGameToProfileData(player_one, player_one_ta, id, winner, loser)
    addGameToProfileData(player_two, player_two_ta, id, winner, loser)

def getNumberOfGamesPlayed():
    count = 0
    games_path = './data/games/'

    for path in os.listdir(games_path):
        if os.path.isfile(os.path.join(games_path, path)):
            count += 1

    return count

def checkForPreviousMatch(player_one, player_two, date):
    num_of_games = getNumberOfGamesPlayed()
    games_path = './data/games/'
    games = []

    for path in os.listdir(games_path):
        if os.path.isfile(os.path.join(games_path, path)):
            f = open(os.path.join(games_path,path))
            data = json.load(f)
            player_one_name = data['players']['player_one']['name']
            player_two_name = data['players']['player_two']['name']

            if data['meta']['date'] == date:
                if player_one_name == player_one and player_two_name == player_two:
                    games.append(data['meta']['game_id'])
                if player_one_name == player_two and player_two_name == player_one:
                    games.append(data['meta']['game_id'])
    
    return len(games) + 1, games

def updatePreviousMatches(prev_game_id, current_game_id):
    with open(f'data/games/{prev_game_id}.json', 'r') as file:
        data = json.load(file)
        data['meta']['following_games'].append(current_game_id)
    
    outfile = json.dumps(data, indent=4)

    with open(f'data/games/{prev_game_id}.json', 'w') as file:
        file.write(outfile)


def createNewGame(player_one_name, player_one_ta, player_one_grade, player_two_name, player_two_ta, player_two_grade, first_mover, first_move, outcome_word, winner_name, winner_ta, winner_grade, loser_name, loser_ta, loser_grade):
    new_game_id = str(uuid.uuid4())
    path = f'data/games/{new_game_id}.json'
    date = datetime.now().strftime("%d/%m/%Y")

    num_prev_games, prev_games = checkForPreviousMatch(player_one_name, player_two_name, date)
    if num_prev_games > 1:
        updatePreviousMatches(prev_games[-1], new_game_id)

    data = {
        "meta": {
            "version": "1.0.4",
            "game_id": new_game_id,
            "date": date,
            "game_number": num_prev_games,
            "previous_games": prev_games,
            "following_games": []
        },
        "players": {
            "player_one": {
                "name": player_one_name,
                "ta": player_one_ta,
                "grade": player_one_grade
            },
            "player_two": {
                "name": player_two_name,
                "ta": player_two_ta,
                "grade": player_two_grade
            }
        },
        "first_mover": first_mover,
        "first_move": first_move,
        "outcome": {
            "outcome_word": outcome_word,
            "winner": {
                "name": winner_name,
                "ta": winner_ta,
                "grade": winner_grade
            },
            "loser":{
                "name": loser_name,
                "ta": loser_ta,
                "grade": loser_grade
            }
        }
    }

    outfile = json.dumps(data, indent=4)

    with open(path, 'w') as f:
        f.write(outfile)

    return path, new_game_id


def newGame():
    player_one, player_one_ta, player_one_grade = cmds.getName('Player 1: ').split('-')
    player_two, player_two_ta, player_two_grade = cmds.getName('Player 2: ').split('-')

    if not os.path.exists(f'data/players/{player_one}-{player_one_ta}.json'):
        player_one_file = createPlayerFile(player_one, player_one_ta, player_one_grade)
    if not os.path.exists(f'data/players/{player_two}-{player_two_ta}.json'):
        player_two_file = createPlayerFile(player_two, player_two_ta, player_two_grade)

    first_mover = input('Who is moving first?: ').lower()
    first_move = input('What was the first move?: ').lower()
    outcome = input('Was the outcome a draw or win?: ').lower()
    if outcome != 'draw':
        winner = input('Who won?: ').lower()
        if winner == player_one:
            winner_ta, winner_grade = player_one_ta, player_one_grade
            loser, loser_ta, loser_grade = player_two, player_two_ta, player_two_grade
        elif winner == player_two:
            winner_ta, winner_grade = player_two_ta, player_two_grade
            loser, loser_ta, loser_grade = player_one, player_one_ta, player_one_grade
    else:
        winner, winner_ta, winner_grade = 'None', 'None', 'None'
        loser, loser_ta, loser_grade = 'None', 'None', 'None'

    path, id = createNewGame(player_one, player_one_ta, player_one_grade, player_two, player_two_ta, player_two_grade, first_mover, first_move, outcome, winner, winner_ta, winner_grade, loser, loser_ta, loser_grade)

    addGameToProfile(player_one, player_one_ta, player_two, player_two_ta, id, winner, loser)

    print(f'Created new game. Check {path} for more.')

    

def createPlayerFile(name, ta, grade):
    date = datetime.now().strftime("%d/%m/%Y")
    with open(f'data/players/{name}-{ta}.json', 'w') as file:
        file_content = {
            "meta": {
                "version": "1.0.1",
                "name": name,
                "ta": ta,
                "grade": grade
            },
            "stats":{
                "played": 0,
                "won": 0,
                "lost": 0,
                "draws": 0
            },
            "last_played": date,
            "games_played":[]
        }

        json.dump(file_content, file, indent=4)

    print(f'Succesfully created player file for {name} in TA {ta}.')

    return f'data/players/{name}-{ta}.json'

main()