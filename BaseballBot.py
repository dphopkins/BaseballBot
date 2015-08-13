import telebot
from datetime import datetime, timedelta
import requests
import json

# THANKS TO fspinillo, casschin, and jonursenbach ON GITHUB FOR THE CODE, WHICH I HAVE EDITED FOR MY PURPOSES

API_TOKEN = '59094683:AAG5mNV5wOSTFq8VjfdU0OlDETvuHMXdgBM'

bot = telebot.TeleBot(API_TOKEN)

diamondbacks = ["Arizona", "Diamondbacks", "ARI"]
braves = ["Atlanta", "Braves", "ATL"]
orioles = ["Baltimore", "Orioles", "BAL"]
red_sox = ["Boston", "Red Sox", "BOS"]
cubs = ["Chicago", "Cubs", "CHC"]
white_sox = ["Chicago", "White Sox", "CWS"]
reds = ["Cincinnati", "Reds", "CIN"]
indians = ["Cleveland", "Indians", "CLE"]
rockies = ["Colorado", "Rockies", "COL"]
tigers = ["Detroit", "Tigers", "DET"]
astros = ["Houston", "Astros", "HOU"]
royals = ["Kansas City", "Royals", "KC"]
angels = ["Los Angeles", "Angels", "LAA"]
dodgers = ["Los Angeles", "Dodgers", "LAD"]
marlins = ["Miami", "Marlins", "MIA"]
brewers = ["Milwaukee", "Brewers", "MIL"]
twins = ["Minnesota" ,"Twins", "MIN"]
mets = ["New York", "Mets", "NYM"]
yankees = ["New York", "Yankees", "NYY"]
athletics = ["Oakland", "Athletics", "OAK"]
phillies = ["Philadelphia", "Phillies", "PHI"]
pirates = ["Pittsburgh", "Pirates", "PIT"]
padres = ["San Diego", "Padres", "SD"]
giants = ["San Francisco", "Giants", "SF"]
mariners = ["Seattle", "Mariners", "SEA"]
cardinals = ["St. Louis", "Cardinals", "STL"]
rays = ["Tampa Bay", "Rays", "TB"]
rangers = ["Texas", "Rangers", "TEX"]
blue_jays = ["Toronto", "Blue Jays", "TOR"]
nationals = ["Washington", "Nationals", "WSH"]

teams = [diamondbacks, braves, orioles, red_sox, cubs, white_sox, reds, indians, rockies, tigers, astros, royals, angels, dodgers, marlins, brewers, twins, mets, yankees, athletics, phillies, pirates, padres, giants, mariners, cardinals, rays, rangers, blue_jays, nationals]

dictionary = {}

for i in range(0, len(teams)):
    city = teams[i][0].upper() # "ARIZONA"
    name = teams[i][1].upper() # "DIAMONDBACKS"
    abbrev = teams[i][2] # "ARI"

    dictionary[city] = abbrev
    dictionary[name] = abbrev
    dictionary[abbrev] = abbrev

alts = ["CHICAGO", "LOS ANGELES", "NEW YORK"]

"""
AL_East = [orioles, red_sox, yankees, rays, blue_jays]
NL_East = [braves, marlins, mets, phillies, nationals]
AL_Central = [white_sox, indians, tigers, royals, twins]
NL_Central = [cubs, reds, brewers, pirates, cardinals]
AL_West = [astros, angels, athletics, mariners, rangers]
NL_West = [diamondbacks, rockies, dodgers, padres, giants]
"""

#function to determine the status of a game, if no team selected
def game_info(game):
    if game['status']['status'] == "In Progress":
        return '%s (%s) vs %s (%s) @ %s %s' % (
                game['away_team_name'],
                game['linescore']['r']['away'],
                game['home_team_name'],
                game['linescore']['r']['home'],
                game['venue'],
                game['status']['status']
            )
    elif (game['status']['status'] == "Final" or game['status']['status'] == "Game Over"):
        return '%s (%s) vs %s (%s) @ %s %s' % (
                game['away_team_name'],
                game['linescore']['r']['away'],
                game['home_team_name'],
                game['linescore']['r']['home'],
                game['venue'],
                game['status']['status']
            )
    elif (game['status']['status'] == "Pre-Game" or game['status']['status'] == "Preview"):
        return '%s vs %s @ %s %s%s %s' % (
                game['away_team_name'],
                game['home_team_name'],
                game['venue'],
                game['home_time'],
                game['hm_lg_ampm'],
                game['status']['status']
            )

#function to determine the status of a game, if a team is selected
def team_score(game):
    if game['status']['status'] == "In Progress":
        return \
        '-------------------------------\n' \
        '%s (%s) vs. %s (%s) @ %s\n' \
        '%s: %s of the %s\n' \
        'Pitching: %s || Batting: %s || S: %s B: %s O: %s\n' \
        '-------------------------------' % (
                game['away_team_name'],
                game['linescore']['r']['away'],
                game['home_team_name'],
                game['linescore']['r']['home'],
                game['venue'],
                game['status']['status'],
                game['status']['inning_state'],
                game['status']['inning'],
                game['pitcher']['last'],
                game['batter']['last'],
                game['status']['s'],
                game['status']['b'],
                game['status']['o']
            )
    elif (game['status']['status'] == "Final" or game['status']['status'] == "Game Over"):
        return \
        '-------------------------------\n' \
        '%s (%s) vs. %s (%s) @ %s\n' \
        'W: %s || L: %s || SV: %s\n' \
        '-------------------------------' % (
                game['away_team_name'],
                game['linescore']['r']['away'],
                game['home_team_name'],
                game['linescore']['r']['home'],
                game['venue'],
                game['winning_pitcher']['name_display_roster'],
                game['losing_pitcher']['name_display_roster'],
                game['save_pitcher']['name_display_roster']
            )
    elif (game['status']['status'] == "Pre-Game" or game['status']['status'] == "Preview"):
        return \
        '-------------------------------\n' \
        '%s vs %s @ %s %s%s\n' \
        'P: %s || P: %s\n' \
        '-------------------------------' % (
                game['away_team_name'],
                game['home_team_name'],
                game['venue'],
                game['home_time'],
                game['hm_lg_ampm'],
                game['away_probable_pitcher']['name_display_roster'],
                game['home_probable_pitcher']['name_display_roster']
               )

#function to determine which feed to grab based on user input
def date_url(date):
    if date == "yesterday":
        baseball_url = "http://gd2.mlb.com/components/game/mlb/year_%d/month_%s/day_%s/master_scoreboard.json" \
        % (now.year, now.strftime("%m"), yesterday.strftime("%d"))
    else:
        baseball_url = "http://gd2.mlb.com/components/game/mlb/year_%d/month_%s/day_%s/master_scoreboard.json" \
                % (now.year, now.strftime("%m"), now.strftime("%d"))
    return baseball_url

# Set date
now = datetime.now()
yesterday = datetime.now() - timedelta(days=1)
day_before = datetime.now() - timedelta(days=2)

# builds data structure from feed
baseball_data = requests.get(date_url("today")).json()
game_array = baseball_data['data']['games']['game']

# Handle '/start' and '/help'
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am BaseballBot!
Use /current to see all current games. You can request to see the score of the most recent game for a specific team by typing in the city, team name, or abbreviation (like PHI for the Phillies).\
""")

# Handle '/clean'
@bot.message_handler(commands=['current'])
def respond(message):
    for game in game_array:
        disp = game_info(game)
        if disp:
            bot.reply_to(message, disp) # currently sends a message per game

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def respond(message):
    txt = message.text.upper()
    if txt in dictionary.keys():
        if txt in alts:
            if txt == "CHICAGO":
                bot.reply_to(message, "Cubs or White Sox?")
            elif txt == "LOS ANGELES":
                bot.reply_to(message, "Angels or Dodgers?")
            elif txt == "NEW YORK":
                bot.reply_to(message, "Mets or Yankees?")
        else:
            response = dictionary.get(txt)
            found = False
            for game in game_array:
                if (game['home_name_abbrev']) == response or (game['away_name_abbrev']) == response:
                    disp = team_score(game)
                    if disp:
                        bot.reply_to(message, disp)
                    found = True
            if found == False:
                bot.reply_to(message, "No games today")
    else:
        bot.reply_to(message, "There was an error. Check your spelling and try again.")

bot.polling()

while True:
    pass