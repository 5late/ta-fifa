# TA FIFA World Cup 2022 Connect-4 Tournament

Data collection on <200 connect-4 games played by 50+ students during TA. Includes stat tracking (personal/ta/grade), single/multi game prediction, and (limited) betting.

See 250+ games [here](./data/games/)

See 50+ student data files [here](./data/players/)

## How it works

### Data Collection

Game is played IRL made up of multiple matches --> Game results are recorded along with some general metadata (who went first, first move) --> Match file is generated --> Match files are linked together

### Data Analysis

Match files are all read and patterns are searched for --> Winrates are noted for each player requested --> Winrates on first move and first to move are noted for each player requested --> Based on the winrate difference from the two players, a different weight is added to each players chance of winning --> If more than 1 match is requested, a function checks how often each player wins multiple games in a row, and determines their "consistency" --> A final weight is acheived --> Fractional odds are generated from the weights --> Decimal odds are generated from the fractional odds --> Implied odds are generated from the decimal odds (These are the %s printed) --> Print results and exit

