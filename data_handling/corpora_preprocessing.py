import os
import re

import numpy as np
import pandas as pd
from tqdm import tqdm

from data_handling.util import CorpusType, files_in_directory


def preprocessing_method_mapping():
    return {
        CorpusType.GoT: preprocess_got_transcripts,
        CorpusType.Cornell: preprocess_cornell_movie_dialogs,
        CorpusType.Parliament: preprocess_parliament_questions,
    }


def compute_request_vectors(rr_pairs, nlp, name=''):
    # unnecessary pipelines
    disabled_pipes = ['tagger', 'parser', 'ner', 'entity_linker', 'entity_ruler', 'textcat',
                      'textcat_multilabel', 'lemmatizer', 'trainable_lemmatizer', 'morphologizer', 'attribute_ruler',
                      'senter', 'sentencizer', 'transformer']

    # define pipeline
    pipeline = nlp.pipe(rr_pairs.request, disable=disabled_pipes, n_process=4, batch_size=1)
    tqdm_desc = '{}: Convert into NLP Vectors'.format(name)
    pipeline = tqdm(pipeline, total=len(rr_pairs.request), unit='Requests', desc=tqdm_desc)

    # apply pipeline
    request_vectors = np.zeros((len(rr_pairs), 300))
    for i, request_document in enumerate(pipeline):
        request_vectors[i][:] = request_document.vector[:]

    return request_vectors


def preprocess_got_transcripts(data_path, nlp, blacklist_regex, csv_name_format, request_vectors_name_format):
    # derive necessary paths
    name = CorpusType.GoT.value
    transcripts_path = os.path.join(data_path, 'Corpora', 'GotTranscripts')
    csv_path = os.path.join(data_path, 'Corpora', csv_name_format.format(name))
    request_vectors_path = os.path.join(data_path, 'Corpora', request_vectors_name_format.format(name))

    # get all episode file paths
    episode_file_paths = files_in_directory(transcripts_path, '**/episode *.txt', recursive=True)

    # define necessary values
    request_reply_pattern = r'(?i)\: ([^\n]*\n*)\btyrion\b(?: lannister)?\:(.*)'
    rr_pairs = pd.DataFrame({'request': [], 'reply': []})

    # read and process episodes
    tqdm_desc = '{}: Read and Process Transcripts'.format(name)
    for episode_file in tqdm(episode_file_paths, unit='Transcripts', desc=tqdm_desc):
        episode = open(episode_file, 'r', encoding='utf8')
        episode_content = episode.read()
        rr_tuples = re.findall(request_reply_pattern, episode_content)
        rr_tuples = [(pair[0].replace('\n', ''), pair[1].replace('\n', '')) for pair in rr_tuples]
        rr_tuples = [pair for pair in rr_tuples if blacklist_regex.search(pair[1]) is None]

        for pair in rr_tuples:
            rr_series = pd.DataFrame({'request': [pair[0].lower()], 'reply': [pair[1]]})
            rr_pairs = pd.concat([rr_pairs, rr_series], ignore_index=True)

    # save csv
    rr_pairs.to_csv(csv_path, index=False)

    # compute request vectors and save them
    request_vectors = compute_request_vectors(rr_pairs, nlp, name)
    np.save(request_vectors_path, request_vectors)


def process_convokit_corpus(data_path, nlp, blacklist_regex, corpus_type, download_name, csv_name_format, request_vectors_name_format):
    # derive necessary paths
    name = corpus_type.value
    data_dir = os.path.join(data_path, 'Corpora', 'Cornell')
    corpus_file = os.path.join(data_dir, 'Corpora', '{}/corpus.json'.format(download_name))
    csv_path = os.path.join(data_path, 'Corpora', csv_name_format.format(name))
    request_vectors_path = os.path.join(data_path, 'Corpora', request_vectors_name_format.format(name))

    # define necessary objects
    rr_pairs = pd.DataFrame({'request': [], 'reply': []})

    # download corpus
    from convokit import Corpus, download
    use_local = os.path.isfile(corpus_file)
    corpus = Corpus(filename=download(download_name, verbose=True, data_dir=data_dir, use_newest_version=True,
                                      use_local=use_local))

    # process all utterances
    tqdm_desc = '{}: Process Utterances'.format(name)
    for key, reply in tqdm(corpus.utterances.items(), unit='Utterances', desc=tqdm_desc):
        if reply.reply_to in corpus.utterances and blacklist_regex.search(reply.text) is None:
            request = corpus.utterances[reply.reply_to]

            rr_series = pd.DataFrame({'request': [request.text.lower()], 'reply': [reply.text]})
            rr_pairs = pd.concat([rr_pairs, rr_series], ignore_index=True)

    # save csv
    rr_pairs.to_csv(csv_path, index=False)

    # compute request vectors and save them
    request_vectors = compute_request_vectors(rr_pairs, nlp, name)
    np.save(request_vectors_path, request_vectors)


def preprocess_cornell_movie_dialogs(data_path, nlp, blacklist_regex, csv_name_format, request_vectors_name_format):
    process_convokit_corpus(data_path, nlp, blacklist_regex, CorpusType.Cornell, 'movie-corpus', csv_name_format,
                            request_vectors_name_format)


def preprocess_parliament_questions(data_path, nlp, blacklist_regex, csv_name_format, request_vectors_name_format):
    process_convokit_corpus(data_path, nlp, blacklist_regex, CorpusType.Parliament, 'parliament-corpus', csv_name_format,
                            request_vectors_name_format)
