import os
from typing import List

import numpy as np
import pandas as pd
import spacy
from tqdm import tqdm

from data_handling.util import CorpusType




class SpacyChatbot:
    def __init__(
            self,
            data_path=os.path.join(os.getcwd(), 'Data'),
            spacy_model='en_core_web_lg',
            csv_name_format='{}_corpus.csv',
            request_vectors_name_format='{}_request_vectors.npy',
    ):
        
        # get spacy nlp model
        if not spacy.util.is_package(spacy_model):
            spacy.cli.download(spacy_model)
        self.nlp = spacy.load(spacy_model)

        # detection of all available corpora
        available_corpora = []
        for corpus_type in CorpusType:
            csv_name = csv_name_format.format(corpus_type.value)
            request_vectors_name = request_vectors_name_format.format(corpus_type.value)
            csv_path = os.path.join(data_path, csv_name)
            request_vectors_path = os.path.join(data_path, request_vectors_name)

            if os.path.isfile(csv_path) and os.path.isfile(request_vectors_path):
                available_corpora.append({'csv_path': csv_path, 'request_vectors_path': request_vectors_path})

        print('Found {} Corp{} {}.'.format(len(available_corpora),
                                           'ora' if len(available_corpora) != 1 else 'us',
                                           [os.path.basename(corpus['csv_path']) for corpus in available_corpora]))

        # load corpora and request vectors
        self.rr_pairs = pd.DataFrame()
        self.request_vectors = np.empty((0, 300), dtype=float)
        for corpus in tqdm(available_corpora, unit='Corpora', desc='Load all Corpora'):
            rr = pd.read_csv(corpus['csv_path'])
            vectors = np.load(corpus['request_vectors_path'])

            self.rr_pairs = pd.concat([self.rr_pairs, rr], ignore_index=True)
            self.request_vectors = np.concatenate([self.request_vectors, vectors], axis=0)

        # be sure that vector values are not 0
        self.request_vectors[np.where(self.request_vectors == 0)] += 0.0000000001

    def __call__(self, request):
        request_doc = self.nlp(request)
        request_vector = request_doc.vector

        similarities = self.database_cosine_similarities(request_vector)
        best_index = np.argmax(similarities)

        return self.rr_pairs.loc[best_index, 'reply']

    def database_cosine_similarities(self, request_vector):
        # be sure that vector values are not 0
        request_vector[np.where(request_vector == 0)] += 0.0000000001

        return np.dot(self.request_vectors, request_vector) / (
                np.linalg.norm(self.request_vectors, axis=1) * np.linalg.norm(request_vector))


if __name__ == "__main__":
    import time

    model = SpacyChatbot()
    example_question = 'Did you hear the king’s in Winterfell?'

    start = time.time()
    print(model(example_question))
    end = time.time()
    print('Seconds needed: {}'.format(end - start))
