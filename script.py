import requests
import shutil
import re
import os
import os.path
from bs4 import BeautifulSoup

# GET NUMBER OF PAGES


def pgnum(pages):
    for link in all_anchors:
        href = str(link.get('href'))
        if href.find('page') >= 0:
            currpages = int((re.findall(r'\d+', href))[-1])
            if currpages > pages:
                pages = currpages
    return pages

# GET THE IMAGE URL AND APPEND IT TO A LIST FROM THE PROVIDED URL


def getlink(url):
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    all_anchors = soup.findAll("img")
    lonk = []
    for link in all_anchors:
        href = str(link.get('src'))
        lonk.append(href)

    for href in lonk:
        if href.startswith('https://images'):
            parts = re.search(
                r'(.*\/\d*\/)(thumb.*?(\d+\.\w+))', href).groups()
            href = parts[0] + parts[-1]
            pic_name = parts[2]
            print(href)
            urllist.append([href, pic_name])

# SAVE THE IMAGES FROM THE LINKS IN THE LIST


def downloader(urllist):
    no = 0
    DEFAULT_DIRECTORY = str(os.getcwd()) + f"/wallpapers"
    os.chdir(DEFAULT_DIRECTORY)
    for item in urllist[0:]:
        pic_url = item[0]
        pic_name = item[1]
        print(item)
        print(str(no) + " from " + str(len(urllist)) + " pictures")
        response = requests.get(pic_url, stream=True)
        os.chdir(DEFAULT_DIRECTORY + "/")
        with open(pic_name, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        os.chdir(DEFAULT_DIRECTORY)
        no += 1
        del response


inp = input("Enter the URL:\n>")
url = f'{inp}&page=1'
baseurl = url[0:url.find('page=')+5]
# print(baseurl)
r = requests.get(url)
soup = BeautifulSoup(r.content, "html.parser")
all_anchors = soup.find_all("a")
pages = -1
pages = pgnum(pages)
print(pages)
urllist = []
if os.path.exists(str(os.getcwd() + "/wallpapers")):
    pass
else:
    os.mkdir("wallpapers")

for each in range(1, pages):
    print(baseurl+str(each))
    getlink(baseurl+str(each))
    print(len(urllist))
    print(str(each) + " from " + str(pages) + " pages")

# LETS DO THIS!
downloader(urllist)
