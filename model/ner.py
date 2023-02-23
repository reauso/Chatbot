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

def substitute_ne(input: str):
    if input:
        nlp = spacy.load("en_core_web_lg")
        ruler = nlp.add_pipe("entity_ruler")

        patterns = read_jsonfile(os.path.normpath(os.getcwd() + '/Data/entity_ruler_patterns.json'))
        ruler.add_patterns(patterns)

        doc = nlp(input)
        for ent in doc.ents:
            if ent.label_ == 'PERSON' or ent.label_ == 'LOC':
                input = input.replace(ent.text, ent.label_)
        return input

def substitute_ne_answer(message: str, answer: str):
    if message and answer:
        nlp = spacy.load("en_core_web_lg")
        ruler = nlp.add_pipe("entity_ruler")

        patterns = read_jsonfile(os.path.normpath(os.getcwd() + '/Data/entity_ruler_patterns.json'))
        ruler.add_patterns(patterns)

        doc_message = nlp(message)
        doc_answer = nlp(answer)
        for ent in doc_answer.ents:
            if ent.label_ == 'PERSON':
                replaced = False
                for message_ent in doc_message.ents:
                    if message_ent.label_ == 'PERSON':
                        answer.replace(ent.text, message_ent.text)
                        replaced = True
                if not replaced:
                    answer.replace(ent.text, 'TODO JSON')
            elif ent.label_ == 'LOC':
                replaced = False
                for message_ent in doc_message.ents:
                    if message_ent.label_ == 'LOC':
                        answer.replace(ent.text, message_ent.text)
                    replaced = True
                if not replaced:
                    answer.replace(ent.text, 'TODO JSON')
