##########
##########
##########
from urllib2 import urlopen
from bs4 import BeautifulSoup

import pymysql

conn = pymysql.connect(host='localhost', user='root', passwd= None, db='mysql', charset='utf8')
cur = conn.cursor()
cur.execute("USE reuter")

# get information of tag "a"
pages = set()

def store(title, contents, time):
	cur.execute("INSERT INTO pages (title, content, pub_time) VALUES (\"%s\", \"%s\", \"%s\")", (title,contents, time))
	cur.connection.commit()

def getLinks(listUrl):
	html = urlopen("http://www.reuters.com/news/archive/" + listUrl)
	bsObj = BeautifulSoup(html.read(), "html.parser")
	headLine = bsObj.find("div", {"class":"news-headline-list"})
	toNextPage = bsObj.find("a", {"class":"control-nav-next"})

	for link in headLine.findAll("a"):
		if link.attrs['href'] not in pages:
			newPage = link.attrs['href']
			pages.add(newPage)
			print newPage
			getArticleDetail(newPage)

	nextListUrl = toNextPage.attrs['href']
	print nextListUrl
	if nextListUrl == "?view=page&page=3&pageSize=10":
		cur.close()
		conn.close()
	else:
		getLinks(nextListUrl)


def getArticleDetail(articleUrl):
	html = urlopen("http://www.reuters.com" + articleUrl)
	bsObj = BeautifulSoup(html.read(), "html.parser")
	title = bsObj.body.h1.get_text()
	contents = bsObj.find("span", {"id":"article-text"}).get_text()
	time = bsObj.find("span", {"class":"timestamp"}).get_text()
	store(title, contents, time)


getLinks("?view=page&page=1&pageSize=10")

