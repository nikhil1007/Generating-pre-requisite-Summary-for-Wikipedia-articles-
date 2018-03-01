from urllib.request import urlopen
# A library in python to extract the data from html, xml documents
from bs4 import BeautifulSoup
import re
import datetime
import string
from urllib.parse import unquote
from rake_nltk import Rake 
import wikipedia

# Function to extract info and rank the keywords in a list
def extractKeywordsUsingRake(subject):
	#Wikipedia module extracts summary from the subject
	extractedText = wikipedia.page(subject).content
	r = Rake()
	# Extract keywords in the form of a list
	r.extract_keywords_from_text(extractedText)
	# Rank the keywords in the list
	l = r.get_ranked_phrases()
	return l

# Text Processing for enforcing encodings
def cleanupLatinEncoding(word):
    try:
        return unquote(word, errors='strict')
    except UnicodeDecodeError:
        return unquote(word, encoding='latin-1')

# A function to get urls within the page
def getLinks(url):
	# Append the url tag to wiki
	html = urlopen("https://en.wikipedia.org"+url)
	bsObj = BeautifulSoup(html, "lxml")
	newLinks = list()
	# The url tags are always i) found in bodycontent tag
	for each in bsObj.findAll("div", {"id": "bodyContent"}):
		#print(each)
		# ii) start with /wiki/
		# and iii) do not contain semicolons
		for link in bsObj.findAll("a", href=re.compile("^(/wiki/)((?!:).)*$")):
			#print(link)
			if 'href' in link.attrs:
				#print(link)
				stripped = re.sub('/wiki/', "", link.attrs['href'])
				stripped = re.sub('_', " ", stripped)
				stripped = cleanupLatinEncoding(stripped)
				newLinks.append(stripped)
	return newLinks


# A function to create the link in parsable format
# wikipedia url is in the form : https://en.wikipedia.org/wiki/Papa_CJ
def linkify(s):
	starting = '/wiki/'
	tokens = s.split(" ")
	for i in range(0, len(tokens)):
		# To append the underscore
		if i != 0:
			starting = starting + '_'
		# To append the words
		starting = starting+tokens[i]
	return starting

# A function to extract initial contents of Wikipedia page
def extractTextData(keyword):
	text =  wikipedia.summary(keyword)
	return text