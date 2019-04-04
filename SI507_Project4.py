from bs4 import BeautifulSoup # need beautifulsoup for scraping
import requests, json # need these to access data on the internet and deal with structured data in my cache
import csv
from advanced_expiry_caching import Cache # use tool from the other file for caching

# Details
# For each state, you should scrape data representing all National Sites (which come in many "types" -- National Parks, National Monuments, National Forests, National Military Parks… etc).
# You should end up with data about a long list of parks that includes these attributes for each:

# ------------------------------------------------

# Name of site
# Type of site (e.g. "National Park" or "National Forest" , etc)
# Description of site (the sentence/short paragraph describing the site), if it exists
# Location value of site (which could be e.g. "AL" or could be a city like "Daviston, AL" or could be a list of states like "LA, MS, FL", etc)

# ------------------------------------------------

# CHALLENGE - State (name or abbreviation -- but be consistent throughout! -- of the state(s) that the site is in)
# You should save this data in a .CSV file such that each row represents 1 national site.
#
# You must
# Use caching for all of your data so you don't make too many requests to the site (indeed, it is fine if you cache all the data you're using just one time and rely on your cached data for the whole project).
# Reasonably handle errors -- so your code will work if you run it and deal with common "weird" things about the site in any reasonable way you choose (e.g. replacing weird values with "NONE" or "", or literally anything else -- just come up with a systematic way to handle weird situations)



FILENAME = "SI507_Proj4_cache.json" # saved in variable with convention of all-caps constant

program_cache = Cache(FILENAME) # create a cache -- stored in a file of this name



url = "https://www.nps.gov/index.htm"

data = program_cache.get(url)
if not data:

    data = requests.get(url).text
    #print(data) # to prove it - this will print out a lot

    # set data in cache:
    program_cache.set(url, data, expire_in_days=1) # just 1 day here because news site / for an example in class

# now data stored in variable -- can do stuff with it, separate from the caching
soup = BeautifulSoup(data, "html.parser") # html.parser string argument tells BeautifulSoup that it should work in the nice html way

# print(soup.prettify()) # view the "pretty" version of everything in the BeautifulSoup instance

#print(soup.find_all("a")) # see if this works...

# All the list items on the page
# list_items =  soup.find_all("li")
# print(list_items)

urllist = []

for link in soup.find_all('a'):
    urllist.append(link.get('href'))

stateurls = urllist[7:14]

listoffullurl = []
for newurl in stateurls:
    listoffullurl.append("http://nps.gov" + newurl) #creates a list of the state urls






def parsingfunct(url): #function parses the state's site for everything we need

    data2 = program_cache.get(url)
    if not data2:

        data2 = requests.get(url).text
        #print(data) # to prove it - this will print out a lot

        # set data in cache:
        program_cache.set(url, data2, expire_in_days=1)

    soup2 = BeautifulSoup(data2, "html.parser")
    #
    #
    # All the list items on the page
    list_items =  soup2.find_all("li")

    datalist = []

    for item in list_items:

        if item.find("h2") != None: #removes the None values
            site_type = (item.h2.string)
            datalist.append(site_type)
            #Name of site
        if item.find("h3") != None: #removes the None values
            site_name = item.h3.string
            datalist.append(site_name)
        # Details of site
        if item.find("p") != None: #removes the None values
            site_details = (item.p.string)
            datalist.append(site_details)
        #Location of site
        if item.find("h4") != None: #removes the None values
            site_location = (item.h4.string)
            datalist.append(site_location)

    return(datalist)


fulldata = []
for indiurl in listoffullurl:
    fulldata.append(parsingfunct(indiurl))
# print(len(fulldata))


# CSV Writer
with open("npsinfo2.csv", "w",newline="") as f:
	writer = csv.writer(f)
	writer.writerow(fulldata)
