'''
Stevem Stapleton 
October 10th

Program implements a web scraper to grab all links from an initial link and never stops.
Links are stripped to domain then saved to a log.txt file.
'''

#imports
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import io
import urllib
import inspect, os
import _thread
import time
import sys

workers = []
name = ""
prev = []
holder = []
goBack = False
root = ""
blackList = ['http://facebook.com/' + 'https://cnn.com/', 'https://www.facebook.com/', 'http://twitter.com/', 'https://www.pinterest.com/', 'http://bleacherreport.com/', 'https://tumblr.com/', 'https://www.linkedin.com/', 'https://youtube.com/', 'https://google.com/', 'https://bit.ly/', 'https://t.co/', 
'https://espn.com/',
'https://bbc.co.uk/'];
visited = []

dontGoback = []
prefix = ""
	
def getHtml(link):	
	#Get html
	html = None
	if(link in blackList):
		return html
	try:
		
		#Get html from url
		page = urlopen(link).read()
		unicode_str = page.decode('utf8', 'ignore')
		html = unicode_str.encode("utf8")
		return html
	except:
		return html
	return html

			
def getUrls(html, logFile):
	global prev
	global goBack
	goBack = False
	global visited
	global dontGoback
	tempList = []
	soup = BeautifulSoup(html, 'html.parser')
	
	for link in soup.find_all('a'):
		url = link.get('href')
		
		if(url != '#' or url != None):
			parsed_uri = urlparse(url)
			domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
			
			if(not(domain in blackList) and not(url in dontGoback)):
				#Check if link is valid
				if(getHtml(domain) != None and domain != ":///"):
					
					logFile.close()
					logFile = open(name, "a+")
					
					if(not(prefix in domain) and (domain not in blackList) and (domain not in logFile)):
						#Check if a valid link
						if(domain not in visited):
							logFile.write(domain + "\n")
							visited.append(domain)
					else:
						prev.append(url)
						tempList.append(url)
						
			
						
	return	tempList
		

def getFile(fileName):
	#Check if user enterx txt if not add it
	if ".txt" not in fileName:
		fileName = fileName + '.txt'
    
	try:
		#Open file if it exists
		file = open(fileName, "r+")
	except:
		#Create file if it does not exist
		file = open(fileName,'a')
		file.close
		file = open(fileName, "r+")
	
	#Clear buffer
	file.flush()
	return file

def start(link, logFile):
	global goBack
	global blackList
	global prev
	
	lastVisited = ""
	tempList = [link]
	while(True):
		
		for link in tempList:
			newHtml = getHtml(link)
			if(newHtml != None and not(link in blackList)):	
				tempList = getUrls(newHtml, logFile)
											
				if(len(tempList) == 0 ):
					goBack = True
							
				logFile.close()
				logFile = open(name, "r+")
				
				for linker in tempList:
					start(linker, logFile)
			lastVisited = link
		
		del prev[len(prev) -1]
		temp = prev[len(prev)-1]
		
		start(temp, logFile)	

def main():
	global name
	global blackList
	global root
	global prefix
	global workers
	
	i = 0
	help = "-w For current workers\n" + "-wN Create new worker\n" + "-q Quit program\n"
	print("Welcome!!!, Type help for options.\n")
	print(help)
	while(True):
		print("WebCrawler \n")
		request = input()
		if("help" in request):
			print(help)
		elif(request == "-w"):
			if(not workers):
				print("No current workers\n")
			for worker in workers:
				print(worker + "\n")				
		elif(request == "-wN"):
			print("Create new worker\n\n")
				
			#Get link
			while(True):
				print("Please enter a link")
				link = input()
				root = link
				html = getHtml(link)
				
				if(html == None):
					if(getHtml('http://' + link) == None):
						print("Invalid link please enter a new link")
					else:
						link = 'http://' + link
						root = link
						break
				else:
					break
					
			#Get logs file
			print("\nPlease enter a text file to output to. Note if it doesnt exist it wil be created.")
			name = input()
			if ".txt" not in name:
				name = name + '.txt'
			logFile = getFile(name)
			
			print("logs file is in -->" + os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))) # script directory)
			print("Note an example link is http://www.cnn.com \nPlease Enter a url to start from")
			
			print("enter prefix you would like to avoid. Ie entering cnn will not save sites with cnn in them but will navigate to them")
			prefix = input()
			
			# Create new thread
			#try:
			print("\nWeb crawler started\n")
			i += 1
			_thread.start_new_thread( start, (link, logFile, ) )
			workers.append("Worker " + str(i) + ": " + link)
			#except:
			#	print("Error: unable to start thread")
		elif(request == "-q"):
			print("Program closing")
			sys.exit()
		else:
			print("Invalid input")
		
main()