from bs4 import BeautifulSoup, SoupStrainer
import requests

# this function returns all links from requested URI
# return type: array
def getLinks(uri):
    # returning array
    links = []

    page = requests.get(uri)
    data = page.text
    soup = BeautifulSoup(data)

    # extract href="" values from <a> tags
    for source in soup.find_all('a'):
        links.append(source.get('href'))
    
    return links