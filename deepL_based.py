# -*- coding: utf-8 -*-
# coding: utf-8
import spacy
from spacy.lang.fr.examples import sentences
import random
from spacy.util import minibatch, compounding
from pathlib import Path
import json

import fr_core_news_md, fr_core_news_sm
from spacy.training.example import Example
import os
from request_info_speech import Information

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"




# nlp = spacy.load('fr_core_news-sm')

class DeepL_recog():

    def __init__(self):
        self.train = []
        self.disable_pipe = []

    # @property
    # def train(self):
    #     return self.train
    #
    # @train.setter
    # def train(self, val):
    #     self.train = val
    #
    # @property
    # def def_pipeline(self):
    #     return self.train()
    #
    # @def_pipeline.setter
    # def def_pipeline(self, value):
    #     self.def_pipeline = value

    def _dl_load_json_transform(self):
        # Load Json file
        with open('./training.json', 'r') as f:
            data = json.load(f)

        # format file
        for ele in data['tag']:
            self.train.append((ele.get('text'), {"entities": [tuple(elem) for elem in ele.get('entities')]}))

    def dl_def_pipeline(self):
        ner = nlp.get_pipe("ner")

        for _, annotation in self.train:
            for ent in annotation.get("entities"):
                ner.add_label(ent[2])

        pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
        self.disable_pipe = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]

    def dl_training(self):
        with nlp.disable_pipes(*self.disable_pipe):
            optimizer = nlp.resume_training()

            for iterration in range(100):
                random.shuffle(self.train)
                losses = {}

                batches = minibatch(self.train, size=compounding(1.0, 4.0, 1.001))

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

    def dl_recog_ents(self, ent):
        info = Information()
        # Make sure the doc.ents is not empty first
        category = ["IT","BADGE","PROPRETE","CLIMATISATION"]
        if ent.label_ in category:
            info.set_category(ent.label_)

        if ent.label_ == "LIEU":
            info.set_place(ent.label_)

        if ent.label_ == "AUTHEUR":
            info.set_author(ent.label_)



# for text, _ in train:
#     print(text)
#     doc = nlp(text)
#     print('Entities', [(ent.text, ent.label_) for ent in doc.ents])

if __name__ == "__main__":
    nlp = fr_core_news_sm.load()

    deepl_train = DeepL_recog()

    deepl_train._dl_load_json_transform()
    deepl_train.dl_def_pipeline()
    deepl_train.dl_training()

    doc = nlp("la climatisation ne fonctionne plus ")
    print('Entities', [(ent.text, ent.label_) for ent in doc.ents])

    # while True:
    #     request = input("En quoi pouvons nous vous aider ? ")
    #
    #     doc = nlp(request)
    #
    #     if not doc.ents:
    #         # Enrégistrer dans un fichier Json categorie autre
    #         print("Aucune entité reconnue")
    #     else:
    #         for ent in doc.ents:
    #             deepl_train.recog_ents()
    #         #print('Entities', [(ent.text, ent.label_) for ent in doc.ents])
