#Scrapes Robert Frost Poems from poetry.com
#url ranges for frost poems: https://www.poetry.com/poem/30819 - 30952
import requests
from bs4 import BeautifulSoup, NavigableString

def getPoem(url):
	"""
		input: poem url
		obtain title, poem, format poem, write title & poem to file
	"""
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	soup=removeDefinition(soup)
	title=soup.find(id='disp-poem-title')
	f.write('Title:'+''.join(title.contents)+'\n\n\n')
	print("Scraping poem:"+''.join(title.contents))
	poem=soup.find(id='disp-quote-body')
	poemString=reformatPoem(poem)
	f.write(poemString)
	f.write('---')

def removeDefinition(poem):
	"""
		remove a tags with links to definition
	"""
	for tag in poem.findAll(True):
	    if tag.name in ['a','h2','em']:
	        s = ""
	        for c in tag.contents:
	            if not isinstance(c, NavigableString):
	                c = removeDefinition(c)
	            s += str(c)

	        tag.replaceWith(s)
	return poem

def reformatPoem(poem):
	"""
		reformat poem by replacing brs with \ns
	"""
	poemString=''
	for i in poem:
		if i.name in ['br']:
			poemString+='\n'
		else:
			poemString+=i
	return poemString

if __name__=="__main__":
	baseURL='https://www.poetry.com/poem/'
	urlRange=range(30819,30953)
	f = open("botbertFrost.txt", "a")
	for url in urlRange:
		#for each poem
		getPoem('https://www.poetry.com/poem/'+str(url))
	f.close()
	print('Done Scraping')


