import os
import os.path as path
import re

import util

if __name__ == "__main__":
    os.chdir(path.dirname(path.dirname(path.realpath(__file__))))
    transcripts_path = path.join(os.getcwd(), 'Data', 'Transcripts')

    # get all episode file paths
    episode_file_paths = util.files_in_directory(transcripts_path, '**/episode *.txt', recursive=True)

    # define necessary regex
    tyrion_pattern = re.compile('tyrion*.+:')

    # read and process episodes
    for episode_file in episode_file_paths:
        episode = open(episode_file, 'r', encoding='utf8')
        episode_lines = episode.readlines()

        for line, line_content in enumerate(episode_lines):
            if re.match(tyrion_pattern, line_content.lower()):
                print('{}, {}, line: {}, content: {}'.format(path.basename(path.dirname(episode_file)),
                                                             path.splitext(path.basename(episode_file))[0], line,
                                                             line_content[:-1]))
