

try:
	import psycopg2, json
	import warnings
	import snscrape.modules.twitter as sntwitter
except Exception as e:
	print("Something went wrong while module loading")
	print("Please install required modules from `requirements.txt`")
	print("`pip3 install -r requirements.txt`")
	exit()


warnings.filterwarnings("ignore")




class TwitterDatasetScrapper():
	def __init__(self, cursor, numberOfPosts: int, keywords: list, since, until, datasetTableName: str):

		'''
		This is a scrapper that will search for tweets by keywords + time intervals and immediately save it to PostgreSQL
		To run the scrapper, it needs:
		1. Cursor, example - (conn = psycopg2.connect(
			host='localhost',
			database='testingtest',
			user='postgres',
			password='mysecretpassword')

			conn.autocommit = True
			cur = conn.cursor()) <- object cur = cursor needed

		2. numberOfPosts (integer) - the number of publications, how many publications we need to search
		IMPORTANT: the expected result might differ from the actual result, due to such factors as a limited number of
		of posts, limitation of the number of requests by the twitter API.
		Tests have shown that your request for 1000 tweets yields 900-950 results

		3. keywords (list) - list of keywords which will be used for the search

		4. since (datetime) - the time from which the search will be carried out (format: YYYY-MM-DD)

		5. until (datetime) - the time up to which the search will be carried out (format: YYYYY-MM-DD)


		Example of startup:
		scrapper = TwitterDatasetScrapper(cur, 50, ['Russia', 'War', 'Ukraine'], '2022-01-01', '2023-01-01')
		scrapper.start()

		In the output we get 50 publications in the format 

		url:rawontent:renderedcontent:publication_date:username:userid:userdisplayname:conversationid:retweetedTweet:quotedTweet:inReplyToTweetId:inReplyToUser:quotedTweet



		Just call the start() method. In this case, scrapper function will be started, which will scrap data from twitter and
		instantly write to the database.

		
		The raw data in JSON format is stored in a list() type array called data2insertSorted.


		'''
		try:
			'''
			Initialize the required variables
			'''
			self.cur = cursor
			self.posts = int(numberOfPosts)
			self.keywords = list(keywords)
			self.since = since
			self.until = until
			self.datasetTableName = str(datasetTableName)

			self.data2insertSorted = list()
			self.dictTweet = dict()
			self.newDictTweet = dict()


		except Exception as e:
			print("Error while initialising module")
			print(f"Reason: {e}")
			exit()


	def start(self):

		'''
		This function allows you to quickly start the scrapper with the ability to 
		instantly write to the database.
		The function is experimental and pre-calculated.

		With this method, writing information to the database is faster 
		than with the first method (where data is first collected in its full scope and then written)
		'''


		dictKeys = dict()
		dictKeys['url'] = None
		dictKeys['rawContent'] = None
		dictKeys['renderedContent'] = None
		dictKeys['publication_date'] = None
		dictKeys['username'] = None
		dictKeys['userID'] = None
		dictKeys['userDisplayName'] = None
		dictKeys['conversationId'] = None
		dictKeys['retweetedTweet'] = None
		dictKeys['inReplyToTweetId'] = None
		dictKeys['inReplyToUser'] = None
		dictKeys['quotedTweet'] = None
		itemIndex = -1
		'''
		What is itemIndex = -1?
		Every time scrapper scrap for publications, it sorts data to avoid duplicates (line 168)
		If data are duplicated, loop continued, because no new data to insert
		When loop continuing, iteration count increases by one

		If at least one duplicate will be ignored, iteration number will be increased and will call the IndexError exception if used as index value of list to point to new data

		For that purposes, itemIndex variable was created. It only increases when new unique data has been inserted to the list.
		'''






		col = [f"{i} varchar(10485760)" for i in dictKeys.keys()] #Getting line "url varchar(10485760), rawContent varchar(10485760)...quotedTweet varchar(10485760)"
		q = '''CREATE TABLE IF NOT EXISTS {} ({})'''.format(self.datasetTableName,",".join(col))

		self.cur.execute(q) #<-- Querying with line above




		'''
		Adding columns with `for` loop
		'''
		for column in list(dictKeys.keys()):

			self.cur.execute(f"ALTER TABLE {self.datasetTableName} ADD COLUMN IF NOT EXISTS {str(column)} varchar(10485760)")

		
		for iteration, tweet in enumerate(sntwitter.TwitterSearchScraper(f' {self.keywords} since:{self.since} until:{self.until}').get_items()):

			self.dictTweet = json.loads(tweet.json()) #Getting raw JSON-object



			self.newDictTweet['url'] = self.dictTweet['url']
			self.newDictTweet['rawContent'] = self.dictTweet['rawContent']
			self.newDictTweet['renderedContent'] = self.dictTweet['renderedContent']
			self.newDictTweet['publication_date'] = self.dictTweet['date']
			self.newDictTweet['username'] = self.dictTweet['user']['username']
			self.newDictTweet['userID'] = self.dictTweet['user']['id']
			self.newDictTweet['userDisplayName'] = self.dictTweet['user']['displayname']
			self.newDictTweet['conversationId'] = self.dictTweet['conversationId']
			self.newDictTweet['retweetedTweet'] = self.dictTweet['retweetedTweet']
			self.newDictTweet['inReplyToTweetId'] = self.dictTweet['inReplyToTweetId']
			self.newDictTweet['inReplyToUser'] = str(self.dictTweet['inReplyToUser'])
			self.newDictTweet['quotedTweet'] = str(self.dictTweet['quotedTweet'])



			

			#Adding JSON-object only if that object does not exists in the list
			if dict(self.newDictTweet) not in self.data2insertSorted:
				self.data2insertSorted.append(dict(self.newDictTweet))
				itemIndex += 1

			else:
				continue




			keys = [str(i) for i in self.data2insertSorted[itemIndex].keys()]



			#Adding new data to dataset
			query = "INSERT INTO {}({}) VALUES(%(url)s, %(rawContent)s, %(renderedContent)s, %(publication_date)s, %(username)s, %(userID)s, %(userDisplayName)s, %(conversationId)s, %(retweetedTweet)s, %(inReplyToTweetId)s, %(inReplyToUser)s, %(quotedTweet)s)".format(self.datasetTableName,','.join(keys))

			try:

				self.cur.execute(query, self.data2insertSorted[itemIndex])
			
			except Exception as e:
				pass

			#If the iteration number is the same as the requested count of publications, the loop is interrupted
			if iteration == self.posts:

				break


if __name__ == '__main__':


	try:
		conn = psycopg2.connect(
				host='localhost',
				database="testingtest",
				user="postgres",
				password='mysecretpassword')

		conn.autocommit = True
		cur = conn.cursor()

		print("[+] Database...OK")
	except Exception as e:
		print("Failed to connect to database...")
		print(f"Error message: {e}")
		exit()


	scrapper = TwitterDatasetScrapper(cur, 100, ['Russia'], '2022-01-01', '2023-01-10', 'sync5')
	scrapper.start()

