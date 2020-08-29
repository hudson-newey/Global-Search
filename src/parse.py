from bs4 import BeautifulSoup, SoupStrainer
import requests
import urllib

# this function returns all links from requested URI
# return type: array
def getLinks(url):
    # returning array
    links = []

    page = requests.get(url)
    data = page.text
    soup = BeautifulSoup(data)

    # extract href="" values from <a> tags
    for source in soup.find_all('a'):
        links.append(source.get('href'))
    
    return links

# convert URI to URL
def uriToURL(uri):
    return urllib.parse.unquote(urllib.parse.unquote(uri))

# this function parses the tracking URL to find the embeded URL
# to do this, you need to remove all tracking features (which are randomly generated)
def createUsableLink(uri):
    # remove substring and append to page
    uri = uri.replace('/url?q=','')

    # if using google or similar engines you may need to modify this to create a usable URL
    if "&sa=" in uri:
        # find index of "&sa=" url paramiter which breaks the links
        scanningIndex = -1
        scanningIndex = uri.find("&sa=")

        # extract sub-string from to append link
        uri = uri[:-(len(uri)-scanningIndex):]
    
    # return usable link
    return uri