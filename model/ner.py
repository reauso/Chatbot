import os.path
import re
from enum import Enum

import spacy
from tqdm import tqdm

from data_handling.util import read_jsonfile, multi_replace


class EntityLabel(Enum):
    PERSON = 'PERSON'
    LOC = 'LOC'
    GPE = 'GPE'
    ORG = 'ORG'
    PRODUCT = 'PRODUCT'
    MONEY = 'MONEY'


# entities to substitute
entity_labels_for_substitution = [label.value for label in list(EntityLabel)]


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


def substitute_named_entity_in_doc(doc):
    entities = doc.ents
    entities = [ent for ent in entities if ent.label_ in entity_labels_for_substitution]

    if len(entities) == 0:
        return doc.text

    # replace entities
    entities_replacement = {re.escape(ent.text): ent.label_ for ent in entities}
    return multi_replace(doc.text, entities_replacement)


def substitute_named_entity_in_text(text, nlp):
    return substitute_named_entity_in_doc(nlp(text))


def substitute_named_entities_in_rr_pairs(rr_pairs, nlp, name=''):
    rr_pairs.request = substitute_named_entities_in_series(rr_pairs.request, nlp, name, ' Request')
    rr_pairs.reply = substitute_named_entities_in_series(rr_pairs.reply, nlp, name, ' Reply')

    return rr_pairs


def substitute_named_entities_in_series(series, nlp, corpus_name='', data_type_name=''):
    # unnecessary pipelines
    disabled_pipes = ['tagger', 'parser', 'textcat', 'textcat_multilabel', 'lemmatizer', 'trainable_lemmatizer',
                      'morphologizer', 'attribute_ruler', 'senter', 'sentencizer', 'tok2vec', 'transformer']

    # define pipeline
    pipeline = nlp.pipe(series, disable=disabled_pipes, n_process=4, batch_size=1)
    tqdm_desc = '{}: Substitute{} Entities'.format(corpus_name, data_type_name)
    pipeline = tqdm(pipeline, total=len(series), unit='Requests', desc=tqdm_desc)

    # apply pipeline
    for i, doc in enumerate(pipeline):
        entities = doc.ents
        entities = [ent for ent in entities if ent.label_ in entity_labels_for_substitution]

        if len(entities) == 0:
            continue

        # replace entities
        entities_replacement = {re.escape(ent.text): ent.label_ for ent in entities}
        series[i] = multi_replace(doc.text, entities_replacement)

    return series
