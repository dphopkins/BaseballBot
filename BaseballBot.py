import telebot

API_TOKEN = '59094683:AAG5mNV5wOSTFq8VjfdU0OlDETvuHMXdgBM'

bot = telebot.TeleBot(API_TOKEN)

diamondbacks = ["Arizona", "Diamondbacks", "ARI"]
braves = ["Atlanta", "Braves", "ATL"]
orioles = ["Baltimore", "Orioles", "BAL"]
red_sox = ["Boston", "Red Sox", "BOS"]
cubs = ["Chicago", "Cubs", "CHC"]
white_sox = ["Chicago", "White Sox", "CHW"]
reds = ["Cincinnati", "Reds", "CIN"]
indians = ["Cleveland", "Indians", "CLE"]
rockies = ["Colorado", "Rockies", "COL"]
tigers = ["Detroit", "Tigers", "DET"]
marlins = ["Florida", "Marlins", "FLA"]
astros = ["Houston", "Astros", "HOU"]
royals = ["Kansas City", "Royals", "KCR"]
angels = ["Los Angeles", "Angels", "LAA"]
dodgers = ["Los Angeles", "Dodgers", "LAD"]
brewers = ["Milwaukee", "Brewers", "MIL"]
twins = ["Minnesota" ,"Twins", "MIN"]
mets = ["New York", "Mets", "NYM"]
yankees = ["New York", "Yankees", "NYY"]
athletics = ["Oakland", "Athletics", "OAK"]
phillies = ["Philadelphia", "Phillies", "PHI"]
pirates = ["Pittsburgh", "Pirates", "PIT"]
padres = ["San Diego", "Padres", "SDP"]
giants = ["San Francisco", "Giants", "SFG"]
mariners = ["Seattle", "Mariners", "SEA"]
cardinals = ["St. Louis", "Cardinals", "STL"]
rays = ["Tampa Bay", "Rays", "TBR"]
rangers = ["Texas", "Rangers", "TEX"]
blue_jays = ["Toronto", "Blue Jays", "TOR"]
nationals = ["Washington", "Nationals", "WSN"]

teams = [diamondbacks, braves, orioles, red_sox, cubs, white_sox, reds, indians, rockies, tigers, marlins, astros, royals, angels, dodgers, brewers, twins, mets, yankees, athletics, phillies, pirates, padres, giants, mariners, cardinals, rays, rangers, blue_jays, nationals]

dictionary = {}

for i in range(0, len(teams)):
	city = teams[i][0].upper() # "ARIZONA"
	name = teams[i][1].upper() # "DIAMONDBACKS"
	abbrev = teams[i][2] # "ARI"
	full_name = teams[i][0] + " " + teams[i][1] # "Arizona Diamondbacks"

	dictionary[city] = full_name
	dictionary[name] = full_name
	dictionary[abbrev] = full_name

alts = ["CHICAGO", "LOS ANGELES", "NEW YORK"]

"""
AL_East = [orioles, red_sox, yankees, rays, blue_jays]
NL_East = [braves, marlins, mets, phillies, nationals]
AL_Central = [white_sox, indians, tigers, royals, twins]
NL_Central = [cubs, reds, brewers, pirates, cardinals]
AL_West = [astros, angels, athletics, mariners, rangers]
NL_West = [diamondbacks, rockies, dodgers, padres, giants]
"""

# Handle '/start' and '/help'
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am BaseballBot!
Use /current to see all current games. You can request to see the score of the most recent game for a specific team by typing in the city, team name, or abbreviation (like PHI for the Phillies).\
""")

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
			response = dictionary.get(txt) # returns full team name
			bot.reply_to(message, response)
	else:
		bot.reply_to(message, "There was an error. Check your spelling and try again.")

bot.polling()

while True:
    pass