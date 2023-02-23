import os
import pickle

import numpy as np
import pandas as pd
import spacy
from tqdm import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer

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
            csv_path = os.path.join(data_path, 'Corpora', csv_name)
            request_vectors_path = os.path.join(data_path, 'Corpora', request_vectors_name)

            if os.path.isfile(csv_path) and os.path.isfile(request_vectors_path):
                available_corpora.append({'csv_path': csv_path, 'request_vectors_path': request_vectors_path})

        print('Found {} Corp{} {}.'.format(len(available_corpora),
                                           'ora' if len(available_corpora) != 1 else 'us',
                                           [os.path.basename(corpus['csv_path']) for corpus in available_corpora]))

        # load corpora and request vectors
        self.rr_pairs = pd.DataFrame()
        self.spacy_request_vectors = np.empty((0, 300), dtype=float)
        for corpus in tqdm(available_corpora, unit='Corpora', desc='Load all Corpora'):
            rr = pd.read_csv(corpus['csv_path'])
            vectors = np.load(corpus['request_vectors_path'])

            self.rr_pairs = pd.concat([self.rr_pairs, rr.astype(str)], ignore_index=True)
            self.spacy_request_vectors = np.concatenate([self.spacy_request_vectors, vectors], axis=0)

        # be sure that vector values are not 0
        self.spacy_request_vectors[np.where(self.spacy_request_vectors == 0)] += 0.0000000001

        # load tfidf model
        tfidf_path = os.path.join(data_path, 'Model', 'tfidf_model.pickle')
        f = open(tfidf_path, 'rb')
        self.tfidf = pickle.load(f)
        f.close()

        # load tfidf vectors
        tfidf_vectors_path = os.path.join(data_path, 'Corpora', 'tfidf_request_vectors.npy')
        self.tfidf_request_vectors = np.load(tfidf_vectors_path)
        for i in range(self.tfidf_request_vectors.shape[0]):
            zero_indices = np.where(self.spacy_request_vectors[i] == 0)
            self.tfidf_request_vectors[i, zero_indices] += 0.0000000001

    def __call__(self, request):
        spacy_request_doc = self.nlp(request)
        spacy_request_vector = spacy_request_doc.vector

        spacy_similarities = self.database_cosine_similarities(spacy_request_vector, 'spacy')
        spacy_best_index = np.argmax(spacy_similarities)
        #print(self.rr_pairs.loc[spacy_best_index, 'request'])

        tfidf_request_vector = self.tfidf.transform([request]).toarray()
        tfidf_request_vector = tfidf_request_vector.reshape(tfidf_request_vector.shape[1])
        tfidf_similarity = self.database_cosine_similarities(tfidf_request_vector, 'tfidf')
        tfidf_best_index = np.argmax(tfidf_similarity)

        print('spacy: {}'.format(spacy_similarities[spacy_best_index]))
        print('tfidf: {}'.format(tfidf_similarity[tfidf_best_index]))
        print('spacy: {}'.format(self.rr_pairs.loc[spacy_best_index, 'reply']))
        print('tfidf: {}'.format(self.rr_pairs.loc[tfidf_best_index, 'reply']))

        return self.rr_pairs.loc[spacy_best_index, 'reply'], spacy_similarities[spacy_best_index]

    def database_cosine_similarities(self, request_vector, type):
        database = self.spacy_request_vectors if type == 'spacy' else self.tfidf_request_vectors

        # be sure that vector values are not 0
        zero_indices = np.where(request_vector == 0)
        request_vector[zero_indices] += 0.0000000001

        return np.dot(database, request_vector) / (np.linalg.norm(database, axis=1) * np.linalg.norm(request_vector))


if __name__ == "__main__":
    import time

    model = SpacyChatbot()
    example_request = [
        'Did you hear the king’s in Winterfell?',
        'Hello',
        'What are you doing',
        'Do you like cats?',
        'Do you have a cat?',
        'yes',
        'Yes',
        'no',
        'What do you think of Tyrion?',
    ]

    for request in example_request:
        request = request.lower()
        start = time.time()
        reply, similarity = model(request)
        end = time.time()
        print('sec: {:.2f}, sim: {:.4f}, request: {}, reply: {}'.format(end - start, similarity, request, reply))
