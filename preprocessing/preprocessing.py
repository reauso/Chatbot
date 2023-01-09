import os
import re

import numpy as np
import pandas as pd
import spacy
from tqdm import tqdm

import util

if __name__ == "__main__":
    data_path = os.path.join(os.getcwd(), 'Data')
    transcripts_path = os.path.join(data_path, 'GotTranscripts')
    csv_path = os.path.join(data_path, 'qa_got.csv')
    vector_path = os.path.join(data_path, 'question_vectors.npy')

    # get all episode file paths
    episode_file_paths = util.files_in_directory(transcripts_path, '**/episode *.txt', recursive=True)

    # define necessary values
    question_answer_pattern = r'(?i)\: ([^\n]*\n*)\btyrion\b(?: lannister)?\:(.*)'
    qa_pairs = pd.DataFrame({'question': [], 'answer': []})

    # read and process episodes
    for episode_file in episode_file_paths:
        episode = open(episode_file, 'r', encoding='utf8')
        episode_content = episode.read()
        qa_tuples = re.findall(question_answer_pattern, episode_content)
        qa_tuples = [(pair[0].replace('\n', ''), pair[1].replace('\n', '')) for pair in qa_tuples]

        for pair in qa_tuples:
            qa_series = pd.DataFrame({'question': [pair[0]], 'answer': [pair[1]]})
            qa_pairs = pd.concat([qa_pairs, qa_series], ignore_index=True)

    qa_pairs.to_csv(csv_path, index=False)

    # save vectors from spacy
    nlp = spacy.load("en_core_web_lg")
    question_vectors = np.zeros((len(qa_pairs), 300))
    for i, question in enumerate(tqdm(qa_pairs.question)):
        doc = nlp(question)
        question_vectors[i][:] = doc.vector[:]

    np.save(vector_path, question_vectors)

    print(qa_pairs[:10])
    print(len(qa_pairs))
