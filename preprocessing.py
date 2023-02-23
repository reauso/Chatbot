import argparse
import os
import pickle

import numpy as np
import pandas as pd
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from tqdm import tqdm

from data_handling.corpora_preprocessing import preprocessing_method_mapping
from data_handling.util import CorpusType, get_word_blacklist_regex, read_textfile


def train_tfidf_vectorizer(data_path, corpora_data_path, vectorizer_path, csv_name_format, request_vector_name_format):
    rr_pairs = load_all_available_corpora(csv_name_format, corpora_data_path)

    # load stopword list
    stop_word_file = os.path.join(data_path, 'stopword_list.txt')
    stop_words = [line.replace('\n', '') for line in read_textfile(stop_word_file)]
    stop_words = list(set(stop_words))

    # train vectorizer
    tfidf = TfidfVectorizer(min_df=5, max_df=0.2, stop_words=stop_words, max_features=1000)
    tfidf.fit_transform(rr_pairs.request + rr_pairs.reply)

    # generate and save tfidf vectors of all requests
    tfidf_request_vectors = tfidf.transform(rr_pairs.request)
    tfidf_request_vectors = tfidf_request_vectors.toarray().astype(np.float32)
    save_path = os.path.join(corpora_data_path, request_vector_name_format.format('tfidf'))
    np.save(save_path, tfidf_request_vectors)

    # save model
    os.makedirs(vectorizer_path, exist_ok=True)
    f = open(os.path.join(vectorizer_path, 'tfidf_model.pickle'), 'wb')
    pickle.dump(tfidf, f)
    f.close()


def load_all_available_corpora(csv_name_format, data_path):
    available_corpora = []
    for corpus_type in CorpusType:
        csv_name = csv_name_format.format(corpus_type.value)
        csv_path = os.path.join(data_path, csv_name)

        if os.path.isfile(csv_path):
            available_corpora.append({'csv_path': csv_path})

    print('Found {} Corp{} {}.'.format(len(available_corpora),
                                       'ora' if len(available_corpora) != 1 else 'us',
                                       [os.path.basename(corpus['csv_path']) for corpus in available_corpora]))

    # load corpora and request vectors
    rr_pairs = pd.DataFrame()
    for corpus in tqdm(available_corpora, unit='Corpora', desc='Load all Corpora'):
        rr = pd.read_csv(corpus['csv_path'], encoding='utf-8')
        rr_pairs = pd.concat([rr_pairs, rr.astype(str)], ignore_index=True)

    return rr_pairs


if __name__ == "__main__":
    # setup argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', type=str, default=os.path.join(os.getcwd(), 'Data'), required=False)
    parser.add_argument('--with_all', action='store_true', help='Preprocess all types of corpora.')
    parser.add_argument('--with_got', action='store_true', help='Preprocess the got transcripts.')
    parser.add_argument('--with_cornell', action='store_true', help='Preprocess the cornell movie-dialogs corpus.')
    parser.add_argument('--with_parliament', action='store_true', help='Preprocess the Parliament Question Time Corpus.')
    parser.add_argument('--with_daily', action='store_true', help='Preprocess the Daily Dialogs Corpus.')
    args = parser.parse_args()

    # define necessary names
    corpora_path = os.path.join(args.data_path, 'Corpora')
    model_path = os.path.join(args.data_path, 'Model')
    csv_filename_format = '{}_corpus.csv'
    request_vector_filename_format = '{}_request_vectors.npy'
    word_blacklist_file = os.path.join(args.data_path, 'word_blacklist.txt')
    word_blacklist_file = word_blacklist_file if os.path.isfile(word_blacklist_file) else None

    # create necessary objects
    if not spacy.util.is_package("en_core_web_lg"):
        spacy.cli.download("en_core_web_lg")
    nlp_model = spacy.load("en_core_web_lg")

    word_blacklist_regex = get_word_blacklist_regex(word_blacklist_file)

    # collect processes
    all_preprocessing_types = []
    if args.with_got or args.with_all:
        all_preprocessing_types.append(CorpusType.GoT)
    if args.with_cornell or args.with_all:
        all_preprocessing_types.append(CorpusType.Cornell)
    if args.with_parliament or args.with_all:
        all_preprocessing_types.append(CorpusType.Parliament)
    if args.with_daily or args.with_all:
        all_preprocessing_types.append(CorpusType.DailyDialogs)

    # convert to preprocess methods (callable)
    mapping = preprocessing_method_mapping()
    all_preprocessing_methods = [mapping[process_type] for process_type in all_preprocessing_types]

    # preprocess corpora
    for preprocess in all_preprocessing_methods:
        preprocess(corpora_path, nlp_model, word_blacklist_regex, csv_filename_format, request_vector_filename_format)

    # train tfidf model
    train_tfidf_vectorizer(args.data_path, corpora_path, model_path, csv_filename_format, request_vector_filename_format)
