import telebot

API_TOKEN = '59094683:AAG5mNV5wOSTFq8VjfdU0OlDETvuHMXdgBM'

bot = telebot.TeleBot(API_TOKEN)

dictionary = {}

diamondbacks = "Arizona Diamondbacks"
dictionary["ARI"] = diamondbacks
dictionary["Arizona"] = diamondbacks
dictionary["Diamondbacks"] = diamondbacks

braves = "Atlanta Braves"
dictionary["ATL"] = braves
dictionary["Atlanta"] = braves
dictionary["Braves"] = braves

orioles = "Baltimore Orioles"
dictionary["BAL"] = orioles
dictionary["Baltimore"] = orioles
dictionary["Orioles"] = orioles

red_sox = "Boston Red Sox"
dictionary["BOS"] = red_sox
dictionary["Boston"] = red_sox
dictionary["Red Sox"] = red_sox

cubs = "Chicago Cubs"
dictionary["CHC"] = cubs
dictionary["Cubs"] = cubs

white_sox = "Chicago White Sox"
dictionary["CHW"] = white_sox
dictionary["White Sox"] = white_sox

dictionary["Chicago"] = "Cubs?White Sox" # ask for clarification

reds = "Cincinnati Reds"
dictionary["CIN"] = reds
dictionary["Cincinnati"] = reds
dictionary["Reds"] = reds

indians = "Cleveland Indians"
dictionary["CLE"] = indians
dictionary["Cleveland"] = indians
dictionary["Indians"] = indians

rockies = "Colorado Rockies"
dictionary["COL"] = rockies
dictionary["Colorado"] = rockies
dictionary["Rockies"] = rockies

tigers = "Detroit Tigers"
dictionary["DET"] = tigers
dictionary["Detroit"] = tigers
dictionary["Tigers"] = tigers

marlins = "Florida Marlins"
dictionary["FLA"] = marlins
dictionary["Florida"] = marlins
dictionary["Marlins"] = marlins

astros = "Houston Astros"
dictionary["HOU"] = astros
dictionary["Houston"] = astros
dictionary["Astros"] = astros

royals = "Kansas City Royals"
dictionary["KCR"] = royals
dictionary["Kansas City"] = royals
dictionary["Royals"] = royals

angels = "Los Angeles Angels"
dictionary["LAA"] = angels
dictionary["Angels"] = angels

dodgers = "Los Angeles Dodgers"
dictionary["LAD"] = dodgers
dictionary["Dodgers"] = dodgers

dictionary["Los Angeles"] = "Angels?Dodgers" # ask for clarification

brewers = "Milwaukee Brewers"
dictionary["MIL"] = brewers
dictionary["Milwaukee"] = brewers
dictionary["Brewers"] = brewers

twins = "Minnesota Twins"
dictionary["MIN"] = twins
dictionary["Minnesota"] = twins
dictionary["Twins"] = twins

mets = "New York Mets"
dictionary["NYM"] = mets
dictionary["Mets"] = mets

yankees = "New York Yankees"
dictionary["NYY"] = yankees
dictionary["Yankees"] = yankees

dictionary["New York"] = "Mets?Yankees" # ask for clarification

athletics = "Oakland Athletics"
dictionary["OAK"] = athletics
dictionary["Oakland"] = athletics
dictionary["Athletics"] = athletics

phillies = "Philadelphia Phillies"
dictionary["PHI"] = phillies
dictionary["Philadelphia"] = phillies
dictionary["Phillies"] = phillies

pirates = "Pittsburgh Pirates"
dictionary["PIT"] = pirates
dictionary["Pittsburgh"] = pirates
dictionary["Pirates"] = pirates

padres = "San Diego Padres"
dictionary["SDP"] = padres
dictionary["San Diego"] = padres
dictionary["Padres"] = padres

giants = "San Francisco Giants"
dictionary["SFG"] = giants
dictionary["San Francisco"] = giants
dictionary["Giants"] = giants

mariners = "Seattle Mariners"
dictionary["SEA"] = mariners
dictionary["Seattle"] = mariners
dictionary["Mariners"] = mariners

cardinals = "St. Louis Cardinals"
dictionary["STL"] = cardinals
dictionary["St. Louis"] = cardinals
dictionary["Cardinals"] = cardinals

rays = "Tampa Bay Rays"
dictionary["TBR"] = rays
dictionary["Tampa Bay"] = rays
dictionary["Rays"] = rays

rangers = "Texas Rangers"
dictionary["TEX"] = rangers
dictionary["Texas"] = rangers
dictionary["Rangers"] = rangers

blue_jays = "Toronto Blue Jays"
dictionary["TOR"] = blue_jays
dictionary["Toronto"] = blue_jays
dictionary["Blue Jays"] = blue_jays

nationals = "Washington Nationals"
dictionary["WSN"] = nationals
dictionary["Washington"] = nationals
dictionary["Nationals"] = nationals

AL_East = [orioles, red_sox, yankees, rays, blue_jays]
NL_East = [braves, marlins, mets, phillies, nationals]
AL_Central = [white_sox, indians, tigers, royals, twins]
NL_Central = [cubs, reds, brewers, pirates, cardinals]
AL_West = [astros, angels, athletics, mariners, rangers]
NL_West = [diamondbacks, rockies, dodgers, padres, giants]

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
	txt = message.text

	if txt in dictionary.keys():
		if "?" in dictionary.get(txt):
			options = dictionary.get(txt).split("?")
			bot.reply_to(message, options[0] + " or " + options[1] + "?")
		else:
			response = dictionary.get(txt) # returns full team name
			bot.reply_to(message, response)
	else:
		bot.reply_to(message, "There was an error. Check your spelling and try again.")

bot.polling()

while True:
    pass