import telebot
from telebot import types
from datetime import datetime, timedelta
import requests
import json

# uses python-baseball by fspinillo to get scores: https://github.com/fspinillo/python-baseball
# uses pyTelegramBotAPI by eternnoir as a python wrapper for the Telegram Bot API: https://github.com/eternnoir/pyTelegramBotAPI

API_TOKEN = '59094683:AAG5mNV5wOSTFq8VjfdU0OlDETvuHMXdgBM'

#bot = telebot.TeleBot(API_TOKEN)
bot = telebot.TeleBot(API_TOKEN, True, 4)

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

divisions = ["AL WEST", "AL CENTRAL", "AL EAST", "NL WEST", "NL CENTRAL", "NL EAST"]

# determines the status of a game, if no team selected
def game_info(game):
    if game['status']['status'] == "In Progress":
        return 'In Progress: %s (%s) @ %s (%s)' % (
            game['away_team_name'],
            game['linescore']['r']['away'],
            game['home_team_name'],
            game['linescore']['r']['home']
        )
    elif (game['status']['status'] == "Final" or game['status']['status'] == "Game Over"):
        return 'Final: %s (%s) @ %s (%s)' % (
            game['away_team_name'],
            game['linescore']['r']['away'],
            game['home_team_name'],
            game['linescore']['r']['home']           
        )
    elif (game['status']['status'] == "Pre-Game" or game['status']['status'] == "Preview"):
        return \
        'Pre-Game: %s @ %s\n' \
        '%s%s at %s' % (
            game['away_team_name'],
            game['home_team_name'],
            game['home_time'],
            game['hm_lg_ampm'],
            game['venue']
        )

# determines the status of a game if a team is selected
def team_score(game):
    if game['status']['status'] == "In Progress":
        if game['status']['inning'] == "1":
            suffix = "st"
        elif game['status']['inning'] == "2":
            suffix = "nd"
        elif game['status']['inning'] == "3":
            suffix = "rd"
        else:
            suffix = "th"

        return \
        '%s (%s) @ %s (%s)\n' \
        'In Progress: %s of the %s%s\n' \
        'Pitching: %s || Batting: %s\n' \
        'S: %s || B: %s || O: %s' % (
            game['away_team_name'],
            game['linescore']['r']['away'],
            game['home_team_name'],
            game['linescore']['r']['home'],
            game['status']['inning_state'],
            game['status']['inning'],
            suffix,
            game['pitcher']['last'],
            game['batter']['last'],
            game['status']['s'],
            game['status']['b'],
            game['status']['o']
        )
    elif (game['status']['status'] == "Final" or game['status']['status'] == "Game Over"):
        return \
        'Final: %s (%s) @ %s (%s)\n' \
        'W: %s || L: %s || SV: %s' % (
            game['away_team_name'],
            game['linescore']['r']['away'],
            game['home_team_name'],
            game['linescore']['r']['home'],
            game['winning_pitcher']['name_display_roster'],
            game['losing_pitcher']['name_display_roster'],
            game['save_pitcher']['name_display_roster']
        )
    elif (game['status']['status'] == "Pre-Game" or game['status']['status'] == "Preview"):
        return \
        'Pregame: %s @ %s\n' \
        '%s%s at %s\n' \
        'P: %s vs %s' % (
            game['away_team_name'],
            game['home_team_name'],
            game['home_time'],
            game['hm_lg_ampm'],
            game['venue'],
            game['away_probable_pitcher']['name_display_roster'],
            game['home_probable_pitcher']['name_display_roster']
        )

# determines which feed to grab based on user input
def date_url(date):
    baseball_url = "http://gd2.mlb.com/components/game/mlb/year_%d/month_%s/day_%s/master_scoreboard.json" % (now.year, now.strftime("%m"), now.strftime("%d"))
    # for last now.strftime("%d"), use yesterday or day_before instead of now to see games on other days, depending on what date ==
    return baseball_url

# Set date
now = datetime.now()
# yesterday = datetime.now() - timedelta(days=1)
# day_before = datetime.now() - timedelta(days=2)

# builds data structure from feed
baseball_data = requests.get(date_url("today")).json()
game_array = baseball_data['data']['games']['game']

hideKeyboard = types.ReplyKeyboardHide() # if sent as reply_markup, will hide the keyboard

# Handle '/start' and '/help'
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am BaseballBot!
Use /all to see all of today's games or request the score of today's game for a specific team by typing in the city, team name, or abbreviation.\
""", reply_markup=hideKeyboard)

# Handle '/all'
@bot.message_handler(commands=['all'])
def respond(message):
    chat_id = message.chat.id
    response = ""
    for game in game_array:
        entry = game_info(game)
        if entry:
            response = response + entry + "\n\n"
    bot.send_message(chat_id, response, reply_markup=hideKeyboard)

# Handle '/division'
@bot.message_handler(commands=['division'])
def respond(message):
    chat_id = message.chat.id
    division_markup = types.ReplyKeyboardMarkup()
    division_markup.row('AL West', 'AL Central', 'AL East')
    division_markup.row('NL West', 'NL Central', 'NL East')
    bot.send_message(chat_id, "Select which division you'd like to check out:", reply_markup=division_markup)

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def respond(message):
    chat_id = message.chat.id
    txt = message.text.upper()

    if txt in divisions:
        if txt == "AL WEST":
            al_west_markup = types.ReplyKeyboardMarkup()
            al_west_markup.add('HOU', 'LAA', 'OAK', 'SEA', 'TEX')
            bot.send_message(chat_id, "Select the team you want to see:", reply_markup=al_west_markup)
        elif txt == "AL CENTRAL":
            al_central_markup = types.ReplyKeyboardMarkup()
            al_central_markup.add('CWS', 'CLE', 'DET', 'KC', 'MIN')
            bot.send_message(chat_id, "Select the team you want to see:", reply_markup=al_central_markup)
        elif txt == "AL EAST":
            al_east_markup = types.ReplyKeyboardMarkup()
            al_east_markup.add('BAL', 'BOS', 'NYY', 'TB', 'TOR')
            bot.send_message(chat_id, "Select the team you want to see:", reply_markup=al_east_markup)
        elif txt == "NL WEST":
            nl_west_markup = types.ReplyKeyboardMarkup()
            nl_west_markup.add('ARI', 'COL', 'LAD', 'PD', 'SF')
            bot.send_message(chat_id, "Select the team you want to see:", reply_markup=nl_west_markup)
        elif txt == "NL CENTRAL":
            nl_central_markup = types.ReplyKeyboardMarkup()
            nl_central_markup.add('CHC', 'CIN', 'MIL', 'PIT', 'STL')
            bot.send_message(chat_id, "Select the team you want to see:", reply_markup=nl_central_markup)
        elif txt == "NL EAST":
            nl_east_markup = types.ReplyKeyboardMarkup()
            nl_east_markup.add('ATL', 'MIA', 'NYM', 'PHI', 'WSH')
            bot.send_message(chat_id, "Select the team you want to see:", reply_markup=nl_east_markup)

    elif txt in dictionary.keys():
        if txt in alts:
            if txt == "CHICAGO":
                bot.reply_to(message, "Cubs or White Sox?", reply_markup=hideKeyboard)
            elif txt == "LOS ANGELES":
                bot.reply_to(message, "Angels or Dodgers?", reply_markup=hideKeyboard)
            elif txt == "NEW YORK":
                bot.reply_to(message, "Mets or Yankees?", reply_markup=hideKeyboard)
        else:
            response = dictionary.get(txt)
            found = False
            for game in game_array:
                if (game['home_name_abbrev']) == response or (game['away_name_abbrev']) == response:
                    entry = team_score(game)
                    if entry:
                        bot.send_message(chat_id, entry, reply_markup=hideKeyboard)
                    found = True
            if found == False:
                bot.send_message(chat_id, "No games for that team today, sorry!", reply_markup=hideKeyboard)
    else:
        bot.send_message(chat_id, "There was an error. Check your spelling and try again.", reply_markup=hideKeyboard)

bot.polling()

while True:
    pass


################# COMMANDS #################
# /all - see all of today's games
# /division - search for a team by division
# /help - get more info
