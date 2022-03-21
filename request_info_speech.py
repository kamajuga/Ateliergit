import json
from typing import Set, Any

import nltk
from nltk.tokenize import word_tokenize
from collections import Counter
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import string
from Postgre_connection import Database
#from text_to_speech import talk
#from speech_r import listen

db = Database()
def replace_at(word):
    
    if "arobase" in word:
        word = word.replace("arobase",'@')
    # for ele in word:
    #     if ele == "arobase":
    #         word = word.replace(ele, "@")
    # 
    return "".join(word.split())
    
def remove_ponctuation(word):
    punc = '''!()-[]'{};:'"\,<>./?@#$%^&*_~'''

    # Removing punctuations in string
    # Using loop + punctuation string
    for ele in word:
        if ele in punc:
            word = word.replace(ele, "")

    return word

def clean(word):
    stpwords = set(stopwords.words("french"))
    exclude = set(string.punctuation)
    lemma = WordNetLemmatizer()

    if type(word) == type([]):
        word = " ".join(wr for wr in word)

    stop_word_removal = " ".join([i for i in word.lower().split() if i not in stpwords])
    punctuation_removal = ''.join(ch for ch in stop_word_removal if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(wrd) for wrd in punctuation_removal.split())

    return normalized


def return_match(list_of_list, list):
    final_matches = []
    index_of_element = None
    for element in list_of_list:
        # print(element)
        match = [x for x in element if x in list]

        if len(match) > len(final_matches):
            index_of_element = list_of_list.index(element)
            final_matches = match
    return index_of_element, final_matches


class Information:

    def __init__(self):
        self._request_title = ""
        self._category = ""
        self._place = ""
        self._author = ""
        self._comment = ""
        pass

    """
        DEFINING GETTERS AND SETTERS
    """

    def get_request_title(self):
        return self._request_title

    def set_request_title(self, value):
        self._request_title = value
        pass

    def get_category(self):
        return self._category

    def set_category(self, value):
        self._category = value
        pass

    def get_place(self):
        return self._place

    def set_place(self, value):
        self._place = value
        pass

    def get_author(self):
        return self._author

    def set_author(self, value):
        self._author = value
        pass

    def get_comment(self):
        return self._comment

    def set_comment(self, value):
        self._comment = value
        pass

    """
        DEFINE METHODS
    """

    def _load_json(self, path):
        try:
            with open(path) as f:
                return json.load(f)
        except ():
            print("Une erreur s'est produit l'or de l'ouverture du fichier")
            #talk()
            return None
        pass

    def check_infos(self):
        cleaned_title = remove_ponctuation(self.get_request_title())
        self.set_request_title(cleaned_title)

        cleaned_place = remove_ponctuation(self.get_place())
        self.set_place(cleaned_place)

        cleaned_comment = remove_ponctuation(self.get_comment())
        self.set_comment(cleaned_comment)

        if self._request_title != "" and self._category != "" and self._place != "" and self._comment != "":
            db.insert_request_info(self.get_request_title(), self.get_category(), self.get_place(), self.get_comment())

    def Identify(self):

        #talk('Votre nom complet s\'il vous plait:')
        #print("Votre nom complet:")
        #name = listen()

        name = input('Votre nom complet:')

        #talk('Votre numero de téléphone:')
        #print("Votre numéro de téléphone:")
        #number = listen()

        number = input('Votre numero de téléphone:')

        #talk('Votre addresse e-mail:')
        #print("Votre addresse e-mail:")
        #email = listen()

        email = input('Votre addresse e-mail:')
        email = replace_at(email)
        #print(email)

        db.insert_author(name, number, email)

        identity = name + " (" + number + ") " + email

        self.set_author(identity)
        pass

    def write_Category(self):
        text = ""

        print("Quelle est la catégorie de votre Problème (Tapez \"autre\" si categorie non proposée)  :")
        #talk("Quelle est la catégorie de votre Problème (Tapez \"autre\" si categorie non proposée)  :")

        categories_json = self._load_json("./intent.json")

        if categories_json is None:
            print("No file loaded")
        else:
            for i in categories_json.keys():
                text += i + " "
            print(text)

            isInpInCat = False

            while isInpInCat == False:

                category = input()

                if category.upper() in categories_json.keys():
                    self.set_category(category)
                    isInpInCat = True
                    print("C'est noté Merci.")
                    #talk("C'est noté Merci.")

                elif category.upper() == "AUTRE":
                    print("Quelle est votre problème ?")
                    problem = input()
                    # create the function that write in the json file
                else:
                    print("Pas de categorie \"{}\", Veuillez réessayer".format(category.upper()))
        pass

    def PLace(self, place):

        self.set_place(place)
        print("Merci pour cette information")
        pass

    def Category(self, text):
        print("Quelle est la catégorie de votre demande")
        #talk("Quelle est la catégorie de votre demande")

    def Gess_category(self, text):

        category_json = self._load_json("./intent.json")

        document = category_json.values()
        final_doc = [clean(doc).split() for doc in document]
        # print('Final 1',final_doc)

        final_text = clean(text).split()

        # print('Final 2',final_text)

        index, matches = return_match(final_doc, final_text)
        category = list(category_json.keys())
        if index is None:
            print(category[-1])
            #talk("La catégorie de votre demande est: {}".format(category[-1]))
            self.set_category(category[-1])
        else:
            print(category[index])
            #talk("La catégorie de votre demande est: {}".format(category[index]))
            self.set_category(category[index])

        pass

    def Title(self, text):

        self.set_request_title(text)

        self.Gess_category(text)
        pass

    def Comment(self, comment):

        self.set_comment(comment)
        pass

    def Recap_Information(self):
        print("Demandeur: {}".format(self.get_author()))
        #talk("Demandeur: {}".format(self.get_author()))

        print("Objet de la demande: {}".format(self.get_request_title()))
        #talk("Objet de la demande: {}".format(self.get_request_title()))

        print("Catégorie: {}".format(self.get_category()))
        #talk("Catégorie: {}".format(self.get_category()))

        print("Lieu de l'incident: {}".format(self.get_place()))
        #talk("Lieu de l'incident: {}".format(self.get_place()))

        print("Commentaire: {}".format(self.get_comment()))
        #talk("Commentaire: {}".format(self.get_comment()))

        # def Modify(self):
        #     print("")
        pass

    pass


db.close()

if __name__ == '__main__':
    info = Information()

    info.Identify()
    pass
