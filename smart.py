# program is smart

import os
import json

# ta win rate
def taWinRate():
    weathers_played = 0
    weathers_won = 0
    bregar_played = 0
    bregar_won = 0
    sanderson_played = 0
    sanderson_won = 0

    player_files = os.listdir('data/players')

    for file in player_files:
        if file[-4:] == 'json':
            file = 'data/players/' + file
            with open(file, 'r') as f:
                data = json.load(f)

                wins = data['stats']['won']
                played = data['stats']['played']

                ta = data['meta']['ta']

                if ta == '16':
                    weathers_played += int(played)
                    weathers_won += int(wins)
                elif ta == '36':
                    bregar_played += int(played)
                    bregar_won += int(wins)
                elif ta == '47':
                    sanderson_played += int(played)
                    sanderson_won += int(wins)
            
            f.close()

    weathers_win_rate = (weathers_won/weathers_played) * 100
    bregar_win_rate = (bregar_won/bregar_played) * 100
    sanderson_win_rate = (sanderson_won/sanderson_played) * 100

    print("TA 16 winrate: " + str(round(weathers_win_rate, 2)) + "%")
    print("TA 47 winrate: " + str(round(bregar_win_rate, 2)) + "%")
    print("TA 36 winrate: " + str(round(sanderson_win_rate, 2)) + "%")

def gradeWinRate():
    nine_wins = 0
    nine_played = 0
    ten_wins = 0
    ten_played = 0
    eleven_wins = 0
    eleven_played = 0
    twelve_wins = 0
    twelve_played = 0

    player_files = os.listdir('data/players')

    for file in player_files:
        if file[-4:] == 'json':
            file = 'data/players/' + file
            with open(file, 'r') as f:
                data = json.load(f)

                wins = data['stats']['won']
                played = data['stats']['played']

                grade = data['meta']['grade']

                if grade == '9':
                    nine_played += played
                    nine_wins += wins
                elif grade == '10':
                    ten_played += played
                    ten_wins += wins
                elif grade == '11':
                    eleven_played += played
                    eleven_wins += wins
                elif grade == '12':
                    twelve_played += played
                    twelve_wins += wins
            
            f.close()
    
    nine_winrate = (nine_wins/nine_played) * 100
    ten_winrate = (ten_wins/ten_played) * 100
    eleven_winrate = (eleven_wins/eleven_played) * 100
    twelve_winrate = (twelve_wins/twelve_played) * 100

    print(f"Nine winrate: {round(nine_winrate, 2)}%")
    print(f"Ten winrate: {round(ten_winrate, 2)}%")
    print(f"Eleven winrate: {round(eleven_winrate, 2)}%")
    print(f"Twelve winrate: {round(twelve_winrate, 2)}%")