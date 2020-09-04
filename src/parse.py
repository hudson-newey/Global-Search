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
    
    # return all links in the webpage (as array)
    return links

# convert URI to URL
def uriToURL(uri):
    return urllib.parse.unquote(urllib.parse.unquote(uri))

# this function parses the tracking URL to find the embeded URL
# to do this, you need to remove all tracking features (which are randomly generated)
def createUsableLink(uri):
    # remove substring and append to page
    uri = uri.replace('/url?q=','')

    # "?ref_src=" paramiter will always get popped first, as it it always the first url paramiter

    # remove refferal uri's
    # this breaks the translation feature
    if f"%3Fref_src%3D" in uri:
        scanningIndex1 = -1
        scanningIndex1 = uri.find(f"%3Fref_src%3D")

        # extract sub-string and pop from to append link
        
        # minus one has to be added to get "?" character
        uri = uri[:-(len(uri)-scanningIndex1):]

    # if using google or similar engines you may need to modify this to create a usable URL
    if "&sa=" in uri:
        # find index of "&sa=" url paramiter which breaks the links
        scanningIndex2 = -1
        scanningIndex2 = uri.find("&sa=")

        # extract sub-string and pop from to append link
        uri = uri[:-(len(uri)-scanningIndex2):]
    
    # return usable link
    return uri