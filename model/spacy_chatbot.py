import os

import numpy as np
import pandas as pd
import spacy


class SpacyChatbot:
    def __init__(
            self,
            csv_path=os.path.join(os.getcwd(), 'Data', 'qa_got.csv'),
            vector_path=os.path.join(os.getcwd(), 'Data', 'question_vectors.npy'),
            spacy_model='en_core_web_lg'
    ):
        self.csv_path = csv_path
        self.vector_path = vector_path
        if not spacy.util.is_package(spacy_model):
            spacy.cli.download(spacy_model)
        self.nlp = spacy.load(spacy_model)

        self.qa_pairs = pd.read_csv(csv_path)
        self.question_vectors = np.load(vector_path)

    def __call__(self, request):
        request_doc = self.nlp(request)
        request_vector = request_doc.vector

        similarities = self.database_cosine_similarities(request_vector)
        best_index = np.argmax(similarities)

        return self.qa_pairs.loc[best_index, 'answer']

    def database_cosine_similarities(self, request_vector):
        return np.dot(self.question_vectors, request_vector) / (
                    np.linalg.norm(self.question_vectors, axis=1) * np.linalg.norm(request_vector))


if __name__ == "__main__":
    import time
    model = SpacyChatbot()
    start = time.time()
    example_question = 'Did you hear the king’s in Winterfell?'
    end = time.time()

    print(model(example_question))
    print('Seconds needed: {}'.format(end - start))
