import os
import re
import pandas as pd

import util

if __name__ == "__main__":
    data_path = os.path.join(os.getcwd(), 'Data')
    transcripts_path = os.path.join(data_path, 'GotTranscripts')
    csv_path = os.path.join(data_path, 'qa_got.csv')

    # get all episode file paths
    episode_file_paths = util.files_in_directory(transcripts_path, '**/episode *.txt', recursive=True)

    # define necessary values
    question_answer_pattern = r'(?i)\: ([^\n]*\n*)\btyrion\b(?: lannister)?\:(.*)'
    question_answer_pairs = pd.DataFrame({'question': [], 'answer': []})

    # read and process episodes
    for episode_file in episode_file_paths:
        episode = open(episode_file, 'r', encoding='utf8')
        episode_content = episode.read()
        qa_tuples = re.findall(question_answer_pattern, episode_content)
        qa_tuples = [(pair[0].replace('\n', ''), pair[1].replace('\n', '')) for pair in qa_tuples]

        for pair in qa_tuples:
            qa_series = pd.DataFrame({'question': [pair[0]], 'answer': [pair[1]]})
            question_answer_pairs = pd.concat([question_answer_pairs, qa_series], ignore_index=True)

    question_answer_pairs.to_csv(csv_path, index=False)

    print(question_answer_pairs[:10])
    print(len(question_answer_pairs))
