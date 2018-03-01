# Import required support functions from functions.py
from functions import linkify, getLinks, extractKeywordsUsingRake, extractTextData
# Import functions for summarization from extractive.py
from extractive import textRankDriver

subject = input("Enter the name of the personality\n").strip()

# Get link
pageLink = linkify(subject)

#List of hyperlinks present in the subject
linkList = getLinks(pageLink)

#List of relevant keywords from Rake
dataList = extractKeywordsUsingRake(subject)
dataList = [x.lower() for x in dataList]
keywordSet = set([x for x in linkList if x.lower() in dataList])

for each in keywordSet:
	if each != subject:
		text = extractTextData(each)
		print("\n"+each+":")
		print(textRankDriver(text))