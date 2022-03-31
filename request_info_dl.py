import json
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import string
from Postgre_connection import Database
from json_dump import dump_unknown_text
# from Email import send_mail
# Email sending
import smtplib
from unidecode import unidecode

"""
    IMPORT FOR DEEPL 
"""
import random
from spacy.util import minibatch, compounding

import fr_core_news_sm
from spacy.training.example import Example
import os

nlp = fr_core_news_sm.load()

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

db = Database()


def replace_at(word):
    if "arobase" in word:
        word = word.replace("arobase", '@')
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

        """
            FOR DEEP LEARNING TRAINNG ONLY
        """
        self.train = []
        self.disable_pipe = []
        self.text = ""
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
        GETTER AND SETTER FOR DL TRAINING ONLY
    """

    def get_train(self):
        return self.train

    def set_train(self, value):
        self.train = value
        pass

    def get_disable_pipe(self):
        return self.disable_pipe

    def set_disable_pipe(self, value):
        self.disable_pipe = value
        pass

    """
        DEFINE METHODS DEEPL ONLY
    """

    def _dl_load_json_transform(self):
        # Load Json file
        with open('./training.json', 'r') as f:
            data = json.load(f)
            pass

        # format file
        for ele in data['tag']:
            self.train.append((ele.get('text'), {"entities": [tuple(elem) for elem in ele.get('entities')]}))

        pass

    def dl_def_pipeline(self):

        ner = nlp.get_pipe("ner")

        for _, annotation in self.get_train():
            for ent in annotation.get("entities"):
                ner.add_label(ent[2])

        pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
        self.set_disable_pipe([pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions])

    pass

    def dl_training(self):
        with nlp.disable_pipes(*self.get_disable_pipe()):
            optimizer = nlp.resume_training()

            for iterration in range(100):
                random.shuffle(self.get_train())
                losses = {}

                batches = minibatch(self.get_train(), size=compounding(1.0, 4.0, 1.001))

                for batch in batches:
                    texts, annotations = zip(*batch)

                    example = []
                    # Update the model with iterating each text
                    for i in range(len(texts)):
                        doc = nlp.make_doc(texts[i])
                        example.append(Example.from_dict(doc, annotations[i]))

                    # Update the model
                    nlp.update(example, drop=0.5, losses=losses)

                    # print("Losses", losses)

    pass

    def dl_recognize_entities(self, text):
        self.text = text

        category = ["IT", "BADGE", "PROPRETE", "CLIMATISATION"]
        doc = nlp(text)
        if not doc.ents:
            # Enrégistrer dans un fichier Json categorie autre
            dump_unknown_text(text)
        else:
            for ent in doc.ents:
                print(ent.text, ent.label_)
                if ent.label_ in category:
                    self.set_category(ent.label_)
                else:
                    if ent.label_ not in ['LIEU', 'AUTHEUR', 'TELEPHONE']:
                        self.set_category('AUTRE')
                        # insert 'resquest' in json category 'AUTRE'
                        dump_unknown_text(text)
                        # send_mail(text)

                if ent.label_ == "LIEU":
                    self.set_place(ent.text)

                if ent.label_ == "AUTHEUR":
                    self.set_author(ent.text)

    """
        DEFINE METHODS
    """

    #def send_mail(self, unknown_text):


    def _load_json(self, path):
        try:
            with open(path) as f:
                return json.load(f)
        except ():
            print("Une erreur s'est produit l'or de l'ouverture du fichier")
            return None
        pass

    def reset_informations(self):
        # we don't reset sel.author because it is consider that the same user can do as much request as he want.
        self.set_request_title("")
        self.set_category("")
        self.set_place("")
        self.set_comment("")

    def check_empty_information(self):
        if not self.get_request_title():
            inp = input("Quel est l'objet de votre demande:")
            if not inp:
                inp = "non renseigné"
            self.set_request_title(inp)
        while not self.get_place():
            self.PLace(input("Quel est le lieu de l'incident?"))
        if not self.get_category():
            cat = input(
                "quelle est la categorie de votre demande :(IT, PROPRETE, BADGE, CLIMATISATION ou AUTRE)").upper()
            if cat not in ["IT", "BADGE", "PROPRETE", "CLIMATISATION"]:
                cat = "AUTRE"
                dump_unknown_text(self.text)
                # self.send_mail(self.text)
            self.set_category(cat)
        if not self.get_author():
            self.Identify()
        if not self.get_comment():
            self.Comment(input("Un commentaire a ajouter? :"))
        self.clean_user_information()

    def clean_user_information(self):
        # Cleans the user's informations and insert in the database
        cleaned_title = remove_ponctuation(self.get_request_title())
        self.set_request_title(cleaned_title)

        cleaned_place = remove_ponctuation(self.get_place())
        self.set_place(cleaned_place)

        cleaned_comment = remove_ponctuation(self.get_comment())
        self.set_comment(cleaned_comment)

        if self._request_title != "" and self._category != "" and self._place != "":
            # comment doesn't have to be given
            db.insert_request_info(self.get_request_title(), self.get_category(), self.get_place(), self.get_comment())
            #self.send_mail(self.text)

            gmail_user = 'kotamajuga@gmail.com'
            gmail_password = '@Julius619Gauth2Kotan'

            sent_from = gmail_user
            to = ['kotannoujulius@gmail.com']
            subject = unidecode('Mail Récapitulatif.')
            body = unidecode(
                "\n Autheur de la demande : {} \nCategorie de la demande : {} \nLieu de l'indcident: {} \nCommentaire: {}".format(
                    unidecode(self.get_author()), unidecode(self.get_category()), unidecode(self.get_place()),
                    unidecode(self.get_comment())))

            email_text = """\
                    From: %s
                    To: %s
                    Subject: %s


                    %s
                    """ % (
                sent_from, ", ".join(to), subject, body)
            try:
                smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                smtp_server.ehlo()
                smtp_server.login(gmail_user, gmail_password)
                smtp_server.sendmail(sent_from, to, email_text)
                smtp_server.close()
                # print("Email sent successfully!")
            except Exception as ex:
                print("Something went wrong….", ex)

    def Identify(self):

        name = input('Votre nom complet:')

        number = input('Votre numero de téléphone:')

        email = input('Votre addresse e-mail:')

        email = replace_at(email)

        db.insert_author(name, number, email)

        identity = name + " (" + number + ") " + email

        self.set_author(identity)
        pass

    def write_Category(self):
        text = ""

        print("Quelle est la catégorie de votre Problème (Tapez \"autre\" si categorie non proposée)  :")

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
                    # talk("C'est noté Merci.")

                elif category.upper() == "AUTRE":
                    print("Quelle est votre problème ?")
                    problem = input()
                    # create the function that write in the json file
                else:
                    print("Pas de categorie \"{}\", Veuillez réessayer".format(category.upper()))
        pass

    def PLace(self, place):

        self.set_place(place)
        #print("Merci pour cette information")
        pass

    def Category(self, text):
        print("Quelle est la catégorie de votre demande")

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
            self.set_category(category[-1])
        else:
            print(category[index])
            self.set_category(category[index])

        pass

    def Title(self, text):
        # set the user's request title and guess the category
        self.set_request_title(text)

        self.Gess_category(text)
        pass

    def Comment(self, comment):

        self.set_comment(comment)
        pass

    def Recap_Information(self):
        print("Demandeur: {}".format(self.get_author()))

        print("Objet de la demande: {}".format(self.get_request_title()))

        print("Catégorie: {}".format(self.get_category()))

        print("Lieu de l'incident: {}".format(self.get_place()))

        print("Commentaire: {}".format(self.get_comment()))

        # def Modify(self):
        #     print("")
        pass

    pass


db.close()

if __name__ == '__main__':
    info = Information()
    nlp = fr_core_news_sm.load()

    info._dl_load_json_transform()
    info.dl_def_pipeline()
    info.dl_training()

    # doc = nlp("la climatisation ne fonctionne plus ")
    # print('Entities', [(ent.text, ent.label_) for ent in doc.ents])
    while True:
        request = input("En quoi pouvons nous vous aider ? ")
        if request == "q":
            break

        info.dl_recognize_entities(request)
        info.check_empty_information()
        info.reset_informations()
        # print('Entities', [(ent.text, ent.label_) for ent in doc.ents])

    pass
