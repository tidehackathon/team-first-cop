from snscrape.modules.reddit import RedditSearchScraper
import json, psycopg2



class RedditScrapper():
	def __init__(self, cursor, numberOfPosts: int, keywords: list, since, until, datasetTableName: str):
		'''
		This is a scrapper that will search for reddit posts by keywords + time intervals and immediately save it to PostgreSQL
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
		of posts, limitation of the number of requests by the reddit API.
		Tests have shown that your request for 1000 tweets yields 900-950 results

		3. keywords (list) - list of keywords which will be used for the search

		4. since (datetime) - the time from which the search will be carried out (format: YYYY-MM-DD)

		5. until (datetime) - the time up to which the search will be carried out (format: YYYYY-MM-DD)


		Example of startup:
		scrapper = TwitterDatasetScrapper(cur, 50, ['Russia', 'War', 'Ukraine'], '2022-01-01', '2023-01-01')
		scrapper.start()

		In the output we get 50 publications in the format 

		author:publication_date:id_:link:selftext:subreddit:title:url:body:parentId:parentid_:_type



		Just call the start() method. In this case, scrapper function will be started, which will scrap data from reddit and
		instantly write to the database.


		
		The raw data in JSON format is stored in a list() type array called data2insertSorted.
		
		

		Also, object has been tested for threaded work.
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
			self.redditDataSet = dict()


		except Exception as e:
			print("Error while initialising module")
			print(f"Reason: {e}")
			exit()


	def start(self):


		dictKeys = dict()
		dictKeys['author'] = None
		dictKeys['publication_date'] = None
		dictKeys['id_'] = None
		dictKeys['link'] = None
		dictKeys['selftext'] = None
		dictKeys['subreddit'] = None
		dictKeys['title'] = None
		dictKeys['url'] = None
		dictKeys['body'] = None
		dictKeys['parentId'] = None
		dictKeys['parentid_'] = None
		dictKeys['_type'] = None
		itemIndex = -1

		'''
		What is itemIndex = -1?
		Every time scrapper scrap for publications, it sorts data to avoid duplicates (line 154)
		If data are duplicated, loop continued, because no new data to insert
		When loop continuing, iteration count increases by one

		If at least one duplicate will be ignored, iteration number will be increased and will call the IndexError exception if used as index value of list to point to new data

		For that purposes, itemIndex variable was created. It only increases when new unique data has been inserted to the list.
		'''




		col = [f"{i} varchar(10485760)" for i in dictKeys.keys()] #Getting line "author varchar(10485760), publication_date varchar(10485760)..._type varchar(10485760)"

		q = '''CREATE TABLE IF NOT EXISTS {} ({})'''.format(self.datasetTableName,",".join(col)) 

		self.cur.execute(q) #<-- Querying with line above





		'''
		Adding columns with `for` loop
		'''
		for column in list(dictKeys.keys()):

			self.cur.execute(f"ALTER TABLE {self.datasetTableName} ADD COLUMN IF NOT EXISTS {str(column)} varchar(10485760)")

		for iteration, redditPost in enumerate(RedditSearchScraper(f' {self.keywords} since:{self.since} until:{self.until}').get_items()):

			self.redditDataSet = json.loads(redditPost.json())#Getting raw JSON-object

			#Renaming PostgreSQL keyword
			self.redditDataSet['publication_date'] = self.redditDataSet.pop('date') 
			self.redditDataSet['id_'] = self.redditDataSet.pop('id')






			'''
			Sometimes scrapper returning 5 items in json-objects, sometimes 3, sometimes 8.
			For accurate query, we will mark 'Unreached' values as None.

			To keep good formatting at line 166 && preventing SQLi, this loop was created
			'''
			for key_ in list(dictKeys.keys()):
				try:
					self.redditDataSet[key_] = str(self.redditDataSet[key_])
				except:
					self.redditDataSet[key_] = None





			#Adding JSON-object only if that object does not exists in the list

			if dict(self.redditDataSet) not in self.data2insertSorted:
				self.data2insertSorted.append(dict(self.redditDataSet))
				itemIndex += 1

			else:
				continue #No new data, passing this iter



			keys = [str(i) for i in self.data2insertSorted[itemIndex].keys()] #Converting json keychain to string like 'key1,key2,key3...keyn' -> postgresql query format

			#Adding new data to dataset
			query = "INSERT INTO {}({}) VALUES(%(_type)s, %(author)s, %(body)s, %(parentId)s, %(subreddit)s, %(url)s, %(publication_date)s, %(id_)s, %(link)s, %(selftext)s, %(title)s, %(parentid_)s)".format(self.datasetTableName,','.join(keys))

			try:
				self.cur.execute(query, self.redditDataSet)
			except:
				pass

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


	scrapper = RedditScrapper(cur, 1000000, ['War', 'Russia', 'Ukraine'], '2022-01-01', '2023-01-10', 'reddit5')
	scrapper.start()