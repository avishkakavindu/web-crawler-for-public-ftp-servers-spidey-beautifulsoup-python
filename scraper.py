from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import ssl

# Ignore ssl certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#url: str = "http://185.105.103.101/serial/McMafia/"
url = input('Enter target Url: ').strip()
count: int = 0

fileTypes = (
    '.webm', '.mkv', '.flv', '.avi', '.mov', '.wmv', '.mp4', '.mp4p', '.mp4v', '.mpg', '.mpef', '.mpv', '.mpeg', '.flv',
    '.f4v', '.f4p', '.f4a', '.f4b')

seasons = {}
quality = {}


def getlinks(cUrl):
    html = urlopen(cUrl, context=ctx).read()
    soup = bs(html, "html.parser")
    return soup('a')


def writelinks(parent, link):
    f = open("links.txt", "a")
    f.write(parent + link + "\n")
    f.close()


# get <a> tags from current page
tags = getlinks(url)
print("Available Seasons:")
for tag in tags:
    if tag.get('href', None).lower().endswith(fileTypes):  # if already in file directory
        writelinks(url, tag.get('href', None))
    else:
        link = tag.get('href', None)
        if link == '../':
            continue
        count += 1
        print('\t({}) - Season {}'.format(count, count))
        seasons[str(count)] = link

# request seasons from user
while True:
    try:
        enteredseasons = list(map(str, input("Please select seasons you want(1,2,3,...): ").split(',')))
    except ValueError:
        print("Invalid input!")
    else:
        if len(seasons) <= count:
            seasons = {key: val for key, val in seasons.items() if key in enteredseasons}  # keep wanted seasons only
            break

for val in seasons.values():    # iterate through the selected seasons
    count = 0
    tmpUrl = url
    tmpUrl += val

    # get <a> in the page
    tags = getlinks(tmpUrl)

    print('For season - {}'.format(val.strip('/')))

    tmpQuality = []
    # request quality
    for tag in tags:
        link = tag.get('href', None)
        if link == '../':
            continue
        count += 1

        tmpQuality.append(link)     # list of available quality
        print('\t({}) - Video Quality - {}'.format(count, link.strip('/')))

    # get input for video quality
    while True:
        try:
            reqQuality = int(input("Please select Video Quality you want(1 or 2 or...): "))
        except ValueError:
            print('Invalid Input!')
        else:
            # correct int value ?
            if len(tmpQuality) >= reqQuality > 0:
                quality[val] = tmpQuality[reqQuality - 1]
                tmpQuality = []
                break

for s, q in quality.items():                # s - season, q - quality
    tmpUrl = url + s + q
    tags = getlinks(tmpUrl)

    for tag in tags:
        if tag.get('href', None) == '../':
            continue
        writelinks(tmpUrl, tag.get('href', None))


# quality selection completed
print("All links scraped succesfully!")


