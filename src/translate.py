from googletrans import Translator

# this function is a translation function
# this function assumes the translation language is comming from english
# format: translate({text to translate}, {translate to})
def translate(text, lang):
    # initilize the Google API translator
    translator = Translator()

    translation = translator.translate(text, src="en", dest=lang)
    translatedText = translation.text

    # # debug info
    print(f"{translation.origin} --> {translatedText} ({lang})")
    
    # return translated text as string
    return translatedText
    # return translation.text
