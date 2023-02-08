import argparse
import os

import spacy

from data_handling.corpora_preprocessing import preprocessing_method_mapping
from data_handling.util import CorpusType, get_word_blacklist_regex


if __name__ == "__main__":
    # setup argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', type=str, default=os.path.join(os.getcwd(), 'Data'), required=False)
    parser.add_argument('--with_all', action='store_true', help='Preprocess all types of corpora.')
    parser.add_argument('--with_got', action='store_true', help='Preprocess the got transcripts.')
    parser.add_argument('--with_cornell', action='store_true', help='Preprocess the cornell movie-dialogs corpus.')
    parser.add_argument('--with_parliament', action='store_true', help='Preprocess the Parliament Question Time Corpus.')
    args = parser.parse_args()

    # define necessary names
    csv_filename_format = '{}_corpus.csv'
    request_vector_filename_format = '{}_request_vectors.npy'
    word_blacklist_file = os.path.join(args.data_path, 'word_blacklist.txt')
    word_blacklist_file = word_blacklist_file if os.path.isfile(word_blacklist_file) else None

    # create necessary objects
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

    # convert to preprocess methods (callable)
    mapping = preprocessing_method_mapping()
    all_preprocessing_types = [mapping[process_type] for process_type in all_preprocessing_types]

    # preprocess
    for preprocess in all_preprocessing_types:
        preprocess(args.data_path, nlp_model, word_blacklist_regex, csv_filename_format, request_vector_filename_format)
