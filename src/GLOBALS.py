SERVER_PORT = 8080

# the search provider is the 3rd party app that does all the search processing
# the results are parsed and all links are extracted from the source page
SEARCH_PROVIDER = "https://www.google.com/search?q="

# LANGUAGES that the program searches in
# LEGEND: german, chinese (simplified)
LANGUAGES = ["de", "zh-cn"]

# the translation provider is a 3rd party add that automatically translates websites into english (or desired language)
# the translation will be done to all unknown LANGUAGES

# possible translation provider: https://translate.google.com/translate?sl=auto&tl=en&u=
TRANSLATION_PROVIDER = "https://translate.google.com/translate?sl=auto&tl=en&u="
