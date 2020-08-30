from googletrans import Translator, constants
from pprint import pprint

# initilize the Google API translator
translator = Translator()

# this function is a translation function
# this function assumes the translation language is comming from english
# format: translate({text to translate}, {translate to})
def translate(text, lang):
    translation = translator.translate(text, src="en", dest=lang)

    # debug info
    print(f"{translation.origin} --> {translation.text} ({lang})")
    
    # return translated text as string
    return translation.text