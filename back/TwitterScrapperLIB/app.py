
try:
	import psycopg2, json
	import snscrape.modules.twitter as sntwitter
	from progress.bar import Bar
	from argparse import ArgumentParser,FileType

except Exception as e:
	print("Something went wrong while module loading")
	print("Please install required modules from `requirements.txt`")
	print("`pip3 install -r requirements.txt`")
	exit()


parser = ArgumentParser()
parser.add_argument('--posts', type=int, required=True)
parser.add_argument('--keywords', type=FileType('r'), required=True)
parser.add_argument('--since', required=True, type=str, help="Scrap since: YYYY-MM-DD")
parser.add_argument('--until', required=True, type=str, help="Scrap until: YYYY-MM-DD")
parser.add_argument('--dataset_name', required=True, type=str, help="Dataset Name (table name)")

args = parser.parse_args() 





class TwitterDatasetScrapper():
	def __init__(self, cursor, numberOfPosts, keywords, since, until, datasetTableName):

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
		of posts, limitation of the number of requests by the twitter API, isolation of the posts with quotes, etc.
		Tests have shown that your request for 1000 tweets yields 900-950 results

		3. keywords (list) - list of keywords which will be used for the search

		4. since (datetime) - the time from which the search will be carried out (format: YYYY-MM-DD)

		5. until (datetime) - the time up to which the search will be carried out (format: YYYYY-MM-DD)


		Example of startup:
		scrapper = TwitterDatasetScrapper(cur, 50, ['Russia', 'War', 'Ukraine'], '2022-01-01', '2023-01-01')
		scrapper.startScrapping()

		In the output we get 50 publications in the format 

		url:rawontent:renderedcontent:publication_date:username:userid:userdisplayname:conversationid:retweetedTweet:quotedTweet:inReplyToTweetId:inReplyToUser(id)



		You can run the scrapper in two ways:
		1. Call the forceStartScrapping() method. Then the scrapper does all its work and returns the status in JSON format
		2. Call the scrap(), createDatasetTable(), createDatasetTableColumns() and insertDataToDatasetTable() methods one by one
		In response, each method will return a JSON object with each method's execution status

		For manual processing, all the data after calling the scrap() method will be stored in the object's attributes and can be accessed externally after the scrap() method completes
		
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
			self.datasetTableName = datasetTableName

			self.data2insertSorted = list()
			self.dictTweet = dict()
			self.newDictTweet = dict()
			scrapperBar = Bar('Processing...', max = args.posts)

		except Exception as e:
			print("Error while initialising module")
			print(f"Reason: {e}")

	def scrap(self):

		'''
		Scrapper itself

		Scrapes the publication and absolutely all information about it, according to time interval and keywords.

		Further, it forms a dictionary of the necessary data, given in line 44, because the others are simply not needed/duplicated

		After that, saves each JSON object into a list, but only if it's missing in that list(sorting)


		'''
		scrapperBar = Bar('Processing...', max = args.posts)
		try:
			for iteration, tweet in enumerate(sntwitter.TwitterSearchScraper(f' {self.keywords} since:{self.since} until:{self.until}').get_items()):

				self.dictTweet = json.loads(tweet.json())



				self.newDictTweet['url'] = self.dictTweet['url']
				self.newDictTweet['rawContent'] = self.dictTweet['rawContent'].replace("'", "`")
				self.newDictTweet['renderedContent'] = self.dictTweet['renderedContent'].replace("'", "`")
				self.newDictTweet['publication_date'] = self.dictTweet['date']
				self.newDictTweet['username'] = self.dictTweet['user']['username']
				self.newDictTweet['userID'] = self.dictTweet['user']['id']
				self.newDictTweet['userDisplayName'] = self.dictTweet['user']['displayname']



				self.newDictTweet['conversationId'] = self.dictTweet['conversationId']
				self.newDictTweet['retweetedTweet'] = self.dictTweet['retweetedTweet']
				#self.newDictTweet['quotedTweet'] = self.dictTweet['quotedTweet']
				self.newDictTweet['inReplyToTweetId'] = self.dictTweet['inReplyToTweetId']

				self.newDictTweet['inReplyToUser'] = self.dictTweet['inReplyToUser']['id'] if isinstance(self.dictTweet['inReplyToUser'], dict) else None



				

				#Adding JSON-object only if that object does not exists in the list
				self.data2insertSorted.append(dict(self.newDictTweet)) if dict(self.newDictTweet) not in self.data2insertSorted else None
				scrapperBar.next()

				#If the iteration number is the same as the requested count of publications, the loop is interrupted
				if iteration == self.posts:

					break

			return {'status': 'OK', 'message': 'dataset data scrapped successfully!'}
		except Exception as e:

			return {'status': 'error', 'message': f"error while scrapping dataset data! Reason: {e}"}



	def createDatasetTable(self):
		#If the table is new - create it
		try:
			col = [f"{i} varchar(10000)" for i in self.newDictTweet.keys()]
			q = '''CREATE TABLE IF NOT EXISTS {} ({})'''.format(self.datasetTableName,",".join(col))

			self.cur.execute(q)

			return {'status': 'OK', 'message': f'dataset table created successfully!'}

		except Exception as e:
			return {'status': 'error', 'message': f"error while creating dataset table! Reason: {e}"}


	def createDatasetTableColumns(self):
		#If the table is new and/or missing columns,
		#this function automatically creates columns based on the keys obtained in the JSON objects in the function above
		errors = 0
		for column in list(self.data2insertSorted[0].keys()):

			try:
				self.cur.execute(f"ALTER TABLE {self.datasetTableName} ADD COLUMN IF NOT EXISTS {str(column)} varchar(10000)")


			except Exception as e:
				errors += 1
				continue
		return {'status': 'OK', 'message': f'creating dataset table columns done with {errors} errors!'}

	def insertDataToDatasetTable(self):
		'''
		First, we need to align the keys and values into a list, and then combine separately the keys, separately the lists into strings. 
		Thus, we adjust them to the correct SQL query of the PostgreSQL database
		'''
		queryBar = Bar('Doing SQL queries...', max = args.posts)
		errors = 0
		errorsList = []
		for j in self.data2insertSorted:

			keys = [str(i) for i in j.keys()]
			values = [str(f'"{i}"') for i in j.values()] 


			#After strings created, inserting them one-by-one into out database
			query = "INSERT INTO {}({}) VALUES({})".format(self.datasetTableName,','.join(keys), ','.join(values)).replace('"', "'")



			try:

				self.cur.execute(query)
				queryBar.next()
			except Exception as e:
				errors += 1
				errorsList.append(e)
				queryBar.next()
				continue
		return {'status': 'OK', 'message': f'inserting data to dataset tables done with {errors} errors!', 'errors_': errorsList}




	def forceStartScrapping(self):
		'''
		It's a forced start. 
		The best option if you just want to start collecting information and go for a coffee.
		'''
		try:
			self.scrap()
			self.createDatasetTable()
			self.createDatasetTableColumns()
			self.insertDataToDatasetTable()
			return {'status': 'OK', 'message': 'scrapper did his job successfully! Check your database now!'}
		except Exception as e:
			return {'status': 'error', 'message': f"scrapper failed for some reasons.. Here is one: {e}"}



	def syncStart(self):
		from progress.bar import Bar

		syncStartBar = Bar('Processing...', max=self.posts)


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


		col = [f"{i} varchar(10000)" for i in dictKeys.keys()]
		q = '''CREATE TABLE IF NOT EXISTS {} ({})'''.format(self.datasetTableName,",".join(col))

		self.cur.execute(q)

		for column in list(dictKeys.keys()):

			self.cur.execute(f"ALTER TABLE {self.datasetTableName} ADD COLUMN IF NOT EXISTS {str(column)} varchar(10000)")




		for iteration, tweet in enumerate(sntwitter.TwitterSearchScraper(f' {self.keywords} since:{self.since} until:{self.until}').get_items()):



			self.dictTweet = json.loads(tweet.json())



			self.newDictTweet['url'] = self.dictTweet['url']
			self.newDictTweet['rawContent'] = self.dictTweet['rawContent'].replace("'", "`")
			self.newDictTweet['renderedContent'] = self.dictTweet['renderedContent'].replace("'", "`")
			self.newDictTweet['publication_date'] = self.dictTweet['date']
			self.newDictTweet['username'] = self.dictTweet['user']['username']
			self.newDictTweet['userID'] = self.dictTweet['user']['id']
			self.newDictTweet['userDisplayName'] = self.dictTweet['user']['displayname']
			self.newDictTweet['conversationId'] = self.dictTweet['conversationId']
			self.newDictTweet['retweetedTweet'] = self.dictTweet['retweetedTweet']
			self.newDictTweet['inReplyToTweetId'] = self.dictTweet['inReplyToTweetId']
			self.newDictTweet['inReplyToUser'] = self.dictTweet['inReplyToUser']['id'] if isinstance(self.dictTweet['inReplyToUser'], dict) else None



			

			#Adding JSON-object only if that object does not exists in the list
			self.data2insertSorted.append(dict(self.newDictTweet)) if dict(self.newDictTweet) not in self.data2insertSorted else None




			keys = [str(i) for i in self.data2insertSorted[iteration].keys()]
			values = [str(f'"{i}"') for i in self.data2insertSorted[iteration].values()]


			#values = [str(f'"{i}"') for i in j.values()] 

			try:
				query = "INSERT INTO {}({}) VALUES({})".format(self.datasetTableName,','.join(keys), ','.join(values)).replace('"', "'")

				self.cur.execute(query)
				syncStartBar.next()

			except Exception as e:
				print(f"Error, {e}")
				syncStartBar.next()

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
	except:
		print("Failed to connect to database...")
		exit()


	scrapper = TwitterDatasetScrapper(cur, args.posts, args.keywords, args.since, args.until, args.dataset_name)

	a = scrapper.scrap()

	b = scrapper.createDatasetTable()

	c = scrapper.createDatasetTableColumns()

	d = scrapper.insertDataToDatasetTable()
