import tweepy
CONSUMER_API='enter your own key'
CONSUMER_API_KEY='enter your own key'
SECRET_API='enter your own key'
SECRET_API_KEY='enter your own key'
def login():
	#add credentials
	auth = tweepy.OAuthHandler(CONSUMER_API,CONSUMER_API_KEY)
	auth.set_access_token(SECRET_API,SECRET_API_KEY)
	api = tweepy.API(auth)
	try:
	    api.verify_credentials()
	except:
	    print("Error during authentication")

	# Create API object
	api = tweepy.API(auth, wait_on_rate_limit=True,
	    wait_on_rate_limit_notify=True)
	return api

def skipline(lines, line, i, useCase=1):
	#return true if line to be skipped.
	#usecase 1 - at start of tweet - skip empty lines
	#usecase 2 - in middle of tweet - do not skip empty lines
	if '---Title:' in line:
		return True
	elif not line.strip():
		if useCase==1:
			return True
		else:
			return False
	elif i>0 and '---Title:' in lines[i-1]:
		return True
	else:
		return False

def pickLines(fileName):
	atStart=True
	atEnd=False
	tweet=''
	savedLines=list()
	#open poetry file
	f = open(fileName,'r')
	lines=f.readlines()
	for i, line in enumerate(lines):
		if atStart:
			#Find tweet start point
			if skipline(lines, line, i):
				savedLines.append(line)
				continue
			else:
				#tweet start point found
				atStart=False
		if not atEnd and len(tweet)<280:
			#build tweet
			if not skipline(lines, line, i, 2):
				prevtweet=tweet
				tweet+=line
				savedLines.append(line)
			else:
				#terminate tweet
				atEnd=True
		if atEnd or len(tweet)>=280:
			#terminating tweet
			if len(tweet)>280:
				#reduce tweet size
				tweet=prevtweet
				savedLines.pop()
				break
			else:
				break
	f.close()
	#to delete lines processed for current tweet
	del lines[:len(savedLines)]
	#add deleted lines to the end
	lines.extend(savedLines)
	#restructure poetry file
	f=open(fileName,'w+')
	for line in lines:
		f.write(line)
	f.close()
	return tweet

def runBot():
	#login
	api=login()
	#pick lines
	tweet = pickLines("botbertFrost.txt")
	try:
		#tweet
		api.update_status(tweet)
	except:
		#notify of error
		api.send_direct_message(api.get_user('thesecretholme').id_str,'Botbert is having an issue :/')
		api.send_direct_message(api.get_user('quickhelpmepls').id_str,'Botbert is having an issue :/')

if __name__=="__main__":
	runBot()
