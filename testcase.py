import unittest
import rsscrawler
import SpecialSites

class TestRSSCrawlerFunctions(unittest.TestCase):
	# initiate an object for testing
	def setUp(self):
		self.instance = rsscrawler.rsscrawler()
		self.instance.stopWords = ['shall', 'applause', 'a', 'able', 'about', 'across', 'after', 'all', 'almost', 'also', 'am', 'among', 'an', 'and', 'any', 'are', 'as', 'at', 'be', 'because', 'been', 'but', 'by', 'can', 'cannot', 'could', 'dear', 'did', 'do', 'does', 'either', 'else', 'ever', 'every', 'for', 'from', 'get', 'got', 'had', 'has', 'have', 'he', 'her', 'hers', 'him', 'his', 'how', 'however', 'i', 'if', 'in', 'into', 'is', 'it', 'its', 'just', 'least', 'let', 'like', 'likely', 'may', 'me', 'might', 'most', 'must', 'my', 'neither', 'no', 'nor', 'not', 'of', 'off', 'often', 'on', 'only', 'or', 'other', 'our', 'own', 'rather', 'said', 'say', 'says', 'she', 'should', 'since', 'so', 'some', 'than', 'that', 'the', 'their', 'them', 'then', 'there', 'these', 'they', 'this', 'tis', 'to', 'too', 'twas', 'us', 'wants', 'was', 'we', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'will', 'with', 'would', 'yet', 'you', 'your']
		self.instance.sources = ''
		self.instance.RSSName ='foxnews'
		self.instance.current_path = ''
		self.instance.path = ''
		self.instance.ppath = ''
		# intiate configaration option
		self.instance.config = {"timezonedifference" : 8 ,"wordsFrequency" : 'false',"storagefile":'MERGE.TXT',"specialsites": ['newyorktimes', 'straitstimes'], "multisource": ['blog-en', 'blog-cn']}

		# "wordsFreq" is used to count words that occur in a title .
		self.instance.wordsFreq = {}

	# test a wrong inputting URL source
	def test_fetchXML_wrongURL(self):		
		result = self.instance.fetchXML('www')
		self.assertEqual(result, "wrong url")

	# test a correct inputting URL source
	def test_fetchXML_URL(self):
		result = self.instance.fetchXML('http://feeds.foxnews.com/foxnews/entertainment')
		self.assertTrue(len(result.entries)>0)		

	# test download a whole webpage function with a wrong link
	def test_fetchWebpage_wrongURL(self):
		page,link,file_id = self.instance.fetchWebpage('www')
		self.assertEqual(page, None)

	# test download a whole webpage function with a correct link
	def test_fetchWebpage_URL(self):
		page,link,file_id = self.instance.fetchWebpage('http://www.nus.edu.sg')
		self.assertTrue(len(page)>0)

	# test special processing for special websites, such as, NewYork Times and Straits Times
	def test_specialProcessing(self):
		page,link = SpecialSites.SpecialSites.newyorktimes(None, 'http://www.nytimes.com/glogin?URI=http://www.nytimes.com/2012/06/20/world/leaders-make-little-headway-in-solving-europe-debt-crisis.html?_r=1&ref=global-home')
		self.assertTrue(len(page)>0)
		page,link = SpecialSites.SpecialSites.straitstimes(None, 'http://sphreg.asiaone.com:80/RegAuth2/stpLogin.html?goto=%2Famserver%2Fcdcservlet%3FTARGET%3Dhttp%253A%252F%252Fwww.straitstimes.com%253A80%252FAsia%252FSouth-eastAsia%252FStory%252FSTIStory_812437.html%26IssueInstant%3D2012-06-19T13%253A11%253A30Z%26MinorVersion%3D0%26RequestID%3D1902483079%26MajorVersion%3D1%26ProviderID%3Dhttp%253A%252F%252Fwww.straitstimes.com%253A80%252Famagent')
		self.assertEqual(page, None)

	# test to store fetched wenpage into a html file and update a record file, that is, MERGE.TXT
	def test_storeNewLinkInMERGEandHTML(self):
		page,link,file_id = self.instance.fetchWebpage('http://www.nus.edu.sg')
		result = self.instance.storeNewLinkInMERGEandHTML(file_id,'http://www.nus.edu.sg',page, 'nus',link,link,1, '2012-06-20')
		self.assertEqual(result, None)

	# test the function of downlaoding words frequency record from a database, that is, RSSName.db
	def test_loadWordsFrequency(self):
		result = self.instance.loadWordsFrequency()
		self.assertTrue(result in ('create success', 'load success'))

	# test the function of counting words frequency with a simple string, that is, "test crawler code code"
	def test_calWordsFrequency(self):
		self.instance.loadWordsFrequency()
		result = self.instance.calWordsFrequency('test crawler code code', '20')
		self.assertTrue('test' in result['20'].keys())
		self.assertEqual(result['20']['test'], 1)
		self.assertTrue('crawler' in result['20'].keys())
		self.assertEqual(result['20']['crawler'], 1)
		self.assertTrue('code' in result['20'].keys())
		self.assertEqual(result['20']['code'], 2)		

	# test to create a database , that is, fetchedlinks.db
	def test_createAllFetchedLinks(self):
		result = self.instance.createAllFetchedLinks('fetchedlinks')
		self.assertTrue(str(result) not in ('failed'))

	# test the function of update recorded database , that is, fetchedlinks.db , in terms of the fetched webpages .
	def test_updateNewLinks(self):
		self.instance.createAllFetchedLinks('fetchedlinks')
		result = self.instance.updateNewLinks('fetchedlinks','http://www.nus.edu.sg')
		self.assertEqual(result, 'success')

	# test to fetch a real RSS source ,that is, 'http://feeds.foxnews.com/foxnews/entertainment' .
	def test_fetchNews(self):
		self.instance.sources = ['http://feeds.foxnews.com/foxnews/entertainment']
		result = self.instance.fetchNews()
		self.assertEqual(result, None)

if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(TestRSSCrawlerFunctions)
	unittest.TextTestRunner(verbosity=2).run(suite)