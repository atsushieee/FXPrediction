# from urllib2 import urlopen
# from bs4 import BeautifulSoup
# import re
# import datetime
# import random

# #html = urlopen("http://en.wikipedia.org/wiki/Kevin_Bacon")
# #bsObj = BeautifulSoup(html.read(), "html.parser")
# #
# #for link in bsObj.find("div", {"id": "bodyContent"}).findAll("a", href=re.compile("^(/wiki/)((?!:).)*$")):
# #	if 'href' in link.attrs:
# #		print(link['href'])

# pages = set()
# random.seed(datetime.datetime.now())

# def getInternalLinks(bsObj, includeUrl):
# 	internalLinks = []
# 	#Finds all links that begin with a "/"
# 	for link in bsObj.findAll("a", href=re.compile("^(/|.*"+includeUrl+")")):
# 		if link.attrs['href'] is not None:
# 			if link.attrs['href'] not in internalLinks:
# 				internalLinks.append(link.attrs['href'])
# 	return internalLinks

# def getExternalLinks(bsobj, excludeUrl):
# 	externalLinks = []
# 	for link in bsobj.findAll("a", href=re.compile("^(http|www)((?!"+excludeUrl+").)*$")):
# 		if link.attrs["href"] is not None:
# 			externalLinks.add(link.attrs["href"])
# 	return externalLinks

# def splitAddress(address):
# 	addressParts = address.replace("http://", "").split("/")
# 	return addressParts

# def getRandomExternalLink(startingPage):
# 	html = urlopen(startingPage)
# 	bsobj = BeautifulSoup(html.read(), "html.parser")
# 	externalLinks = getExternalLinks(bsobj, splitAddress(startingPage)[0])
# 	if len(externalLinks) == 0:
# 		print("No external links, looking around the site for one")
# 		domain = urlparse(startingPage).scheme + "://" + urlparse(startingPage).netloc
# 		internalLinks = getInternalLinks(bsobj, domain)
# 		return getRandomExternalLink(internalLinks[random.randint(0,len(internalLinks)-1)])
# 	else:
# 		return externalLinks[random.randint(0, len(externalLinks)-1)]


# def followExternalOnly(startingSite):
# 	externalLink = getRandomExternalLink(startingSite)
# 	print("Random external link is: " + externalLink)
# 	followExternalOnly(externalLink)

# followExternalOnly("http://oreilly.com")


from urllib2 import urlopen
from bs4 import BeautifulSoup
import re
import datetime
import random
import pymysql

random.seed(datetime.datetime.now())

conn = pymysql.connect(host='localhost', user='root', passwd= None, db='mysql', charset='utf8')
cur = conn.cursor()
cur.execute("USE scraping")

def store(title, content):
	cur.execute("INSERT INTO pages (title, content) VALUES (\"%s\",\"%s\")", (title, content))
	cur.connection.commit()

def getLinks(articleUrl):
	html = urlopen("http://en.wikipedia.org" + articleUrl)
	bsObj = BeautifulSoup(html.read(), "html.parser")
	title = bsObj.find("h1").get_text()
	content = bsObj.find("div", {"id":"mw-content-text"}).find("p").get_text()
	store(title, content)
	return bsObj.find("div", {"id":"bodyContent"}).findAll("a",href=re.compile("^(/wiki/)((?!:).)*$"))

links = getLinks("/wiki/Kevin_Bacon")

try:
	while len(links) > 0:
		newArticle = links[random.randint(0, len(links)-1)].attrs["href"]
		print(newArticle)
		links = getLinks(newArticle)
finally:
	cur.close()
	conn.close()