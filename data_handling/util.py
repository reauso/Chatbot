import json
import os.path

import glob
import re
from enum import Enum


class CorpusType(Enum):
    GoT = 'got'  # got transcripts
    Cornell = 'cornell'  # cornell movie dialogs
    Parliament = 'parliament'  # Parliament Question Time Corpus


def files_in_directory(directory_path, file_patterns=None, recursive=False):
    if file_patterns is None:
        file_patterns = ['**']
    elif not isinstance(file_patterns, list):
        file_patterns = [file_patterns]

    files = []
    for pattern in file_patterns:
        files.extend(glob.glob(os.path.join(directory_path, pattern), recursive=recursive))

    return files


def read_textfile(textfile):
    """
    Reads a textfile.
    :param textfile: The textfile path.
    :return: A List containing all lines of content.
    """
    f = open(textfile, 'r')
    text = f.readlines()
    f.close()

    return text


def read_jsonfile(jsonfile):
    """
    Reads a jsonfile.
    :param jsonfile: The jsonfile path.
    :return: The object.
    """
    f = open(jsonfile, 'r')
    json_object = json.load(f)
    f.close()

    return json_object


def get_word_blacklist_regex(blacklist_file):
    word_blacklist = read_textfile(blacklist_file)
    word_blacklist = [line[:-1].lower() for line in word_blacklist]
    word_blacklist = set(word_blacklist)
    word_regex = '|'.join(word_blacklist)
    regex = r'(?i)\b({})\b'.format(word_regex)
    regex = re.compile(regex)

    return regex
