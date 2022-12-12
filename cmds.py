import os
import json

def editProfileGrade(name):
    games = []
    with open('data/players.txt', 'r') as f:
        lines = f.readlines()

        new_grade = input('Input New Grade: ')

        possible = []

        new_lines = []

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
                    possible.clear()
                    possible.append(possibility)
                    realname = possibility.split('-')[0].rstrip()
                    ta = possibility.split('-')[1].rstrip()
                    grade = possibility.split('-')[2].rstrip()

        for each in possible:
            for line in lines:
                if line.rstrip() == each.rstrip():
                    realname = each.split('-')[0].rstrip()
                    ta = each.split('-')[1].rstrip()
                    grade = new_grade
                    new_lines.append(f'{name}-{ta}-{grade}\n')
                else:
                    new_lines.append(line)
        
        f.close()

        with open('data/players.txt', 'w') as file:
            file.write("".join(new_lines))
            print('Succesfully changed grade in players.txt file.')

        file.close()

        with open(f'data/players/{name}-{ta}.json', 'r') as json_file:
            data = json.load(json_file)

            data['meta']['grade'] = new_grade
            for game_played in data['games_played']:
                games.append(game_played)

        json_file.close()
        
        with open(f'data/players/{name}-{ta}.json', 'w') as json_file_writable:
            outfile = json.dumps(data, indent=4)

            json_file_writable.write(outfile)
            print('Successfully changed grade in personal json file.')

        for game in games:
            with open(f'data/games/{game}.json', 'r') as game_file:
                game_data = json.load(game_file)

                if game_data['players']['player_one']['name'] == realname:
                    game_data['players']['player_one']['grade'] = new_grade
                elif game_data['players']['player_two']['name'] == realname:
                    game_data['players']['player_two']['grade'] = new_grade
                else:
                    print(f'Error occured finding name in game file: {game}')
            
            game_file.close()

            with open(f'data/games/{game}.json', 'w') as game_file_writable:
                game_outfile = json.dumps(game_data, indent=4)

                game_file_writable.write(game_outfile)
                print(f'Successfully changed grade in game: {game}')
            
            game_file_writable.close()
                
        
