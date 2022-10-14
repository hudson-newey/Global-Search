import http.server
import socketserver
from urllib.parse import urlparse
from urllib.parse import parse_qs
import glob
import time

# local file imports
from util import rf
from parse import getLinks, createUsableLink, uriToURL
from translate import translate
from GLOBALS import LANGUAGES

# the search provider is the 3rd party app that does all the search processing
# the results are parsed and all links are extracted from the source page
searchProvider = "https://www.google.com/search?q="

# the translation provider is a 3rd party add that automatically translates websites into english (or desired language)
# the translation will be done to all unknown LANGUAGES

# possible translation provider: https://translate.google.com/translate?sl=auto&tl=en&u=
translationProvider = "https://translate.google.com/translate?sl=auto&tl=en&u="

# LOCAL HTTP FILE SERVER (modified to serve web query requests)
class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Sending an '200 OK' response
        self.send_response(200)

        # Setting the header
        self.send_header("Content-type", "text/html")

        # Whenever using 'send_header', you also have to call 'end_headers'
        self.end_headers()

        # Extract query param
        # format: http://localhost:[PORT]/?q=[SEARCHTERM]
        searchTerm = 'null'
        query_components = parse_qs(urlparse(self.path).query)
        if 'q' in query_components:
            searchTerm = query_components["q"][0]

        # if loading external elements, the query will be "null"
        # in this case, break the request and do not process request
        if searchTerm == 'null':
            # debug info
            print("broke away from loading external file")
            return None

        # WEBPAGE
        html = rf("static/index.html")
        html += "<body><p class='resultsList'>"

        # get and display links
        # do english results first
        # "links" variable is a array storing all "native language" links
        links = getLinks(searchProvider + searchTerm)

        # international and global results
        foreignLinks = []
        for language in LANGUAGES:
            translatedTerm = translate(searchTerm, language)
            foreignLinks += getLinks(searchProvider + translatedTerm)
            
            # make the program delayed so you don't get locked out
            # default is 1.2 (seconds)
            time.sleep(0.8)

        # remove all double-ups from search result list
        # this may be due to finding the same results in multipule LANGUAGES
        # (e.g. wikipedia pages are usually universal)
        links = list(dict.fromkeys(links))

        # scan and append all "native language" links to dynamic webpage
        for i in range(len(links)):

            # test that it is a link that we want
            if "/url?q=" in links[i]:
                # remove substring and append to page
                linkToAppend = links[i].replace('/url?q=','')

                # create usable link
                # this is a very complex task
                linkToAppend = createUsableLink(links[i])

                # decode URI to URL
                linkToAppend = uriToURL(linkToAppend)
                
                # append link result to webpage
                html += f"""<a class='websiteLink' href='{linkToAppend}'>{linkToAppend}</a><br>"""
            
            # scanning sequence
            continue

        # scan and append all "foreign websites" links to dynamic webpage
        # these websites require translation of webpages
        for i in range(len(foreignLinks)):

            # test that it is a link that we want
            if "/url?q=" in foreignLinks[i]:
                # remove substring and append to page
                linkToAppend = foreignLinks[i].replace('/url?q=','')

                # create usable link
                # this is a very complex task
                linkToAppend = createUsableLink(foreignLinks[i])

                # decode URI to URL
                linkToAppend = uriToURL(linkToAppend)
                
                # append link result to webpage
                html += f"""<a class='websiteLink' href='{translationProvider}{linkToAppend}'>{linkToAppend}</a><br>"""
            
            # scanning sequence
            continue

        # static webpage html imports
        html += ("</p></body></html><style>"+rf("./static/css/style.css")+"</style>"+
            "<script>"+rf("./static/js/func.js")+"</script>"+
            "<script>"+rf("./static/js/script.js")+"</script>")



        # Writing the HTML contents with UTF-8
        self.wfile.write(bytes(html, "utf8"))
        return

# arg 1 is server port
def startServer(PORT):
    # Create an object of the above class
    handler_object = MyHttpRequestHandler

    my_server = socketserver.TCPServer(("", PORT), handler_object)

    # output statement of the server starting
    print("Started Local Server on port:", PORT)

    # display help prompt
    # http://localhost/:{PORT}?q={QUERY}
    print(f"http://localhost:{PORT}?q=Query")

    # start the server with keep-alive request
    my_server.serve_forever()
