import os

import numpy as np
import pandas as pd
import spacy
from tqdm import tqdm


def keep_token(token):
    return token.is_alpha and not token.is_stop


if __name__ == "__main__":
    csv_path = os.path.join(os.getcwd(), 'Data', 'qa_got.csv')
    qa_pairs = pd.read_csv(csv_path)

    nlp = spacy.load("en_core_web_lg")

    question_vectors = np.zeros((len(qa_pairs), 300))
    question_docs = []
    for i, question in enumerate(tqdm(qa_pairs.question)):
        doc = nlp(question)
        question_vectors[i][:] = doc.vector[:]
        question_docs.append(doc)

    example_question = 'Did you hear the king’s in Winterfell?'
    example_doc = nlp(example_question)
    example_vector = example_doc.vector

    similarity = np.dot(question_vectors, example_vector) / (np.linalg.norm(question_vectors) * np.linalg.norm(example_vector))
    best_index = np.argmax(similarity)

    print(similarity)
    print(similarity.shape)
    print(best_index)
    print(similarity[best_index])
    print(qa_pairs.loc[best_index, 'question'])
    print(qa_pairs.loc[best_index, 'answer'])



