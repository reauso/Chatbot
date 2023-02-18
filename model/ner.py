import os.path

import spacy

from data_handling.util import read_jsonfile


def print_ner(input: str):
    if input:
        nlp = spacy.load("en_core_web_lg")
        ruler = nlp.add_pipe("entity_ruler")

        patterns = read_jsonfile(os.path.normpath(os.getcwd() + '/Data/entity_ruler_patterns.json'))
        ruler.add_patterns(patterns)

        doc = nlp(input)
        print("---- Entities: ")
        for ent in doc.ents:
            print(ent.text, " | ", ent.label_, " | ", spacy.explain(ent.label_))
