import json
import os
import uuid

def main():
    print('What is happening')
    print('1 - New Game')

    choice = input('Enter choice: ')

    if choice == '1':
        newGame()

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
            for possiblility in possible:
                if possiblility.split('-')[1] == correct:
                    ta = possibility.split('-')[1].rstip()
                    grade = possiblility.split('-')[2].rstrip()
        
        return ta, grade

def addGameToProfileData(player, player_ta, id, winner, loser):
    f = open(f'data/players/{player}-{player_ta}.json')
    
    data = json.load(f)

    data['games_played'].append(id)
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

def createNewGame(player_one_name, player_one_ta, player_one_grade, player_two_name, player_two_ta, player_two_grade, first_mover, first_move, outcome_word, winner_name, winner_ta, winner_grade, loser_name, loser_ta, loser_grade):
    new_game_id = str(uuid.uuid4())
    path = f'data/games/{new_game_id}.json'

    data = {
        "meta": {
            "version": "1.0.0",
            "game_id": new_game_id,
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
    player_one = input('Player One: ').lower()
    player_two = input('Player Two: ').lower()

    player_one_ta = input('Player Ones TA #: ')
    player_two_ta = input('Player Twos TA #: ')

    player_one_grade = input('Player Ones Grade: ')
    player_two_grade = input('Player Twos Grade: ')

    if not os.path.exists(f'data/players/{player_one}-{player_one_ta}.json'):
        player_one_file = createPlayerFile(player_one, player_one_ta, player_one_grade)
    if not os.path.exists(f'data/players/{player_two}-{player_two_ta}.json'):
        player_two_file = createPlayerFile(player_two, player_two_ta, player_two_grade)

    first_mover = input('Who is moving first?: ').lower()
    first_move = input('What was the first move?: ').lower()
    outcome = input('Was the outcome a draw or win?: ').lower()
    if outcome != 'draw':
        winner = input('Who won?: ').lower()
        loser = input('Who lost?: ').lower()
    else:
        winner = 'None'
        loser = 'None'

    winner_ta, winner_grade = getPlayerInfo(winner)
    loser_ta, loser_grade = getPlayerInfo(loser)

    path, id = createNewGame(player_one, player_one_ta, player_one_grade, player_two, player_two_ta, player_two_grade, first_mover, first_move, outcome, winner, winner_ta, winner_grade, loser, loser_ta, loser_grade)

    addGameToProfile(player_one, player_one_ta, player_two, player_two_ta, id, winner, loser)

    print(f'Created new game. Check {path} for more.')

    

def createPlayerFile(name, ta, grade):
    with open(f'data/players/{name}-{ta}.json', 'w') as file:
        file_content = {
            "meta": {
                "version": "1.0.0",
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
            "games_played":[]
        }

        json.dump(file_content, file, indent=4)

    print(f'Succesfully created player file for {name} in TA {ta}.')

    return f'data/players/{name}-{ta}.json'

main()