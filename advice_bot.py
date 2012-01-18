import twitter
import random
import time
api = twitter.Api(consumer_key='key', 
	consumer_secret='secret', 
	access_token_key='key', 
	access_token_secret='secret')
# dictionary of keywords to search for and suggestions to reply with.
# format is 'search keyword':['Reply 1', 'Reply 2', etc]

advice = {
	"need haircut":[
		"A pixie cut would look good on you.",
		"Just get an up-do.",
		"Bangs are coming back!",
		"Just grow it out!",
		"Don't cut it, just get a blow out"],
	"change password" :[
		"Your password should be at least 8 characters long.",
		"Visit this site to create a random password for you: http://www.random.org/passwords/",
		"You should consider moving to 2-factor authentication"],
	"bad day" :[
		"Don't worry, tomorrow will be better!",
		"At least you've still got your stunning good looks!",
		"Call your mom, I'm sure you'll feel better after talking to her",
		"Things could always be worse."],
	"too much coffee" :[
		"Maybe you should put less sugar in your coffee",
		"Milk definitely is better in coffee than creamer.",
		"You would sleep better if you didn't drink so much coffee"],
	"get enough sleep" :[
		"You really should go to bed earlier",
		"Maybe try cutting down on the caffeine before bed"],
	"hate my job" :[
		"The country's unemployment is about 9%. You should feel happy!"],
	"drunk last night" :[
		"Hydration is key to avoiding a hangover",
		"Beer before liquor, never been sicker, liquor before beer, you're in the clear!"],
	"wikipedia" :[
                "Unhappy about wikipedia being down? Visit the EFF to learn more: https://blacklist.eff.org/"]
	}

# a dictionary keeping track if you've replied to this tweet before
advised = []
log = open('log.txt', 'a')

while True :
	try : 
		# pull a random item from the advice dictionary to search for
		a = advice.keys()[random.randint(0,len(advice) - 1)]
		# search for the keyword
		tweets = api.GetSearch(a, per_page=100)
		# pull a random search response
		tweet = tweets[random.randint(0,len(tweets) - 1)]
		if tweet.GetId() not in advised :
			api.PostUpdate("@%s %s" % (tweet.GetUser().GetScreenName(), advice[a][random.randint(0, len(advice[a]) - 1)]), tweet.GetId())
			# debugging: prints the user and their message
			log.write("%s %s\n" % (tweet.GetUser().GetScreenName(), tweet.GetText()))
			# debugging: print the reply we are going to send
			log.write("@%s %s\n" % (tweet.GetUser().GetScreenName(), advice[a][random.randint(0, len(advice[a]) - 1)]))
			# add the tweet we just replied to to the reply to dictionary
			advised.append(tweet.GetId())
			# chill out for a little bit, but tweet more frequently in the daytime (5 minutes daytime, 20 minutes after 5pm)
			if time.localtime().tm_hour in range(8,17) :
				time.sleep(300)
			else :
				time.sleep(1200)
		
		# look for mentions, and have a hard-coded response.  pretty much the same logic as above.
		myReplies = api.GetMentions()
		for reply in myReplies :
			if reply.GetId() not in advised :
				api.PostUpdate("@%s I hope that you found my advice helpful!" % reply.GetUser().GetScreenName(), reply.GetId())
				log.write("@%s I hope that you found my advice helpful!\n" % reply.GetUser().GetScreenName())
				advised.append(reply.GetId())
				
		# after 1000 replies, clean out the dictionary	
		if len(advised) > 1000 : advised = []
		
	except KeyboardInterrupt : 
		# accept keyboard interrupts
		quit()
	except :
		# ignore any errors that may come from the main
		# we have run into occasional crashes due to unicode characters, etc
		pass	