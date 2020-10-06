import json
import urllib.request
from bs4 import BeautifulSoup
from tqdm import tqdm

# define constants for the use case
sourceRoot = str("http://www.city-data.com/forum/")
homePage = str(sourceRoot+"search.php?searchid=40860988")
fixedTagOnPage = str("atlanta")
outputFilename = "output/post_content.json"

# get all html content on the homepage
htmlOnPage = urllib.request.urlopen(homePage)
soup = BeautifulSoup(htmlOnPage, "html.parser")

# to store the links to posts on the home page. These links have the tag "atlanta" and are .html
postLinks = []

for link in soup.findAll("a"):
    post = str(link.get("href"))
    if post.find(fixedTagOnPage) != -1 and post.find("html") != -1:
        postLinks.append(post)

# remove duplicates
postLinks = list(dict.fromkeys(postLinks))

postContent = []

# follow each scraped link, and scrape the html content from it
for link in tqdm(postLinks):

    htmlOnPage = urllib.request.urlopen(sourceRoot+link)
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
