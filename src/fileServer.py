import http.server
import socketserver
from urllib.parse import urlparse
from urllib.parse import parse_qs
import time

# local file imports
from util import rf
from parse import getLinks, createUsableLink, uriToURL, websiteTitle
from translate import translate
from GLOBALS import LANGUAGES, SEARCH_PROVIDER, TRANSLATION_PROVIDER

# LOCAL HTTP FILE SERVER (modified to serve web query requests)
class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def serveHTML(self, htmlCode):
        # Writing the HTML contents with UTF-8
        self.wfile.write(bytes(htmlCode, "utf8"))

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
            self.serveHTML(rf("static/index.html"))
            return None

        # WEBPAGE
        html = rf("static/index.html")
        html += "<body><p class='resultsList'>"

        # get and display links
        # do english results first
        # "links" variable is a array storing all "native language" links
        links = getLinks(f"{SEARCH_PROVIDER}{searchTerm}")

        # international and global results
        foreignLinks = []
        for language in LANGUAGES:
            translatedTerm = translate(searchTerm, language)
            foreignLinks += getLinks(f"{SEARCH_PROVIDER}{translatedTerm}")
            
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

                if ("google.com" in linkToAppend):
                    continue
                
                # append link result to webpage
                html += f"""<div class='search-result'>
                <b><h3>{websiteTitle(linkToAppend)}</h3></b><br>
                <a class='websiteLink' href='{linkToAppend}'>{linkToAppend}</a>
                </div>
                <br>"""
            
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

                if ("google.com" in linkToAppend):
                    continue
                
                # append link result to webpage
                html += f"""<div class='search-result'>
                <b><h3>{websiteTitle(TRANSLATION_PROVIDER + linkToAppend)}</h3></b><br>
                <a class='websiteLink' href='{TRANSLATION_PROVIDER}{linkToAppend}'>{linkToAppend}</a>
                </div>
                <br>"""
            
            # scanning sequence
            continue

        # static webpage html imports
        html += ("</p></body></html><style>"+rf("./static/css/dist/style.css")+"</style>"+
            "<script>"+rf("./static/js/dist/func.js")+"</script>"+
            "<script>"+rf("./static/js/dist/script.js")+"</script>")



        self.serveHTML(html)
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
