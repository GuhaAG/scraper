import json
import urllib.request
from bs4 import BeautifulSoup
from tqdm import tqdm

# define constants for the use case
homePage = str("http://www.city-data.com/forum/search.php?searchid=40860988")
fixedTagOnPage = str("atlanta")
outputFilename = "output/post_content.json"

# get all html content on the homepage
htmlOnPage = urllib.request.urlopen(homePage)
soup = BeautifulSoup(htmlOnPage, "html.parser")

# to store the links to threads on the home page.
homeThreadLinks = []
allThreadLinks = []

print("-----------------Gathering Threads--------------")
# find all thread links from the home page
for link in soup.findAll("a"):
    thread = str(link.get("href"))
    if thread.find(fixedTagOnPage) != -1 or thread.find("page=") != -1:
        homeThreadLinks.append("http://www.city-data.com/forum/"+thread)

# add all links to pages from threads
for link in tqdm(homeThreadLinks):

    allThreadLinks.append(link)

    htmlOnPage = urllib.request.urlopen(link)
    soup = BeautifulSoup(htmlOnPage, "html.parser")

    for link2 in soup.findAll("a[class^=smallfont]"):
        thread = str(link2.get("href"))
        if thread.find(fixedTagOnPage) != -1:
            allThreadLinks.append("http://www.city-data.com/"+thread)


# remove duplicates
allThreadLinks = list(dict.fromkeys(allThreadLinks))

# for link in allThreadLinks:
#   print(link)

postContent = []

print("-----------------Parsing Threads--------------")

# follow each scraped link, and scrape the html content from it
for link in tqdm(allThreadLinks):

    htmlOnPage = urllib.request.urlopen(link)
    soup = BeautifulSoup(htmlOnPage, "html.parser")

    for dateDiv, postDiv in zip(soup.select('div[style*="color:#A2B3D0;"]'), soup.select('[id^=post_message]')):
        date = dateDiv.get_text("\n", strip=True).strip()
        content = postDiv.get_text("\n", strip=True).strip()

        postContent.append({
            'date': date,
            'content': content
        })


# write output to json file
with open(outputFilename, "w", encoding="utf8") as outfile:
    json.dump(postContent, outfile)
