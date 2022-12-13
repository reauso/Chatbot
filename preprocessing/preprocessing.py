import os
import os.path as path
import re

import util

if __name__ == "__main__":
    import os
    import os.path as path
    import re

    import util

    if __name__ == "__main__":
        os.chdir(path.dirname(path.dirname(path.realpath(__file__))))
        transcripts_path = path.join(os.getcwd(), 'Data', 'Transcripts')

        # get all episode file paths
        episode_file_paths = util.files_in_directory(transcripts_path, '**/episode *.txt', recursive=True)

        # define necessary values
        question_answer_pattern = r'(?i)\: ([^\n]*\n*)\btyrion\b(?: lannister)?\:(.*)'
        question_answer_pairs = []

        # read and process episodes
        for episode_file in episode_file_paths:
            episode = open(episode_file, 'r', encoding='utf8')
            episode_content = episode.read()

            question_answer_pairs.extend(re.findall(question_answer_pattern, episode_content))

        print(question_answer_pairs[:10])
        print(len(question_answer_pairs))
