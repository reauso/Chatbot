import spacy

from Data.entity_ruler_patterns import patterns


def print_ner(input: str):
    if input:
        nlp = spacy.load("en_core_web_lg")
        ruler = nlp.add_pipe("entity_ruler")

        ruler.add_patterns(patterns)

        doc = nlp(input)
        print("---- Entities: ")
        for ent in doc.ents:
            print(ent.text, " | ", ent.label_, " | ", spacy.explain(ent.label_))

