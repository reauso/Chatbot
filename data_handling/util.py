import json
import os.path

import glob
import re
import zipfile
from enum import Enum
from io import BytesIO

import requests


class CorpusType(Enum):
    GoT = 'got'  # got transcripts
    Cornell = 'cornell'  # cornell movie dialogs
    Parliament = 'parliament'  # Parliament Question Time Corpus
    DailyDialogs = 'dailyDialogs'  # Daily Dialogs Corpus


def files_in_directory(directory_path, file_patterns=None, recursive=False):
    if file_patterns is None:
        file_patterns = ['**']
    elif not isinstance(file_patterns, list):
        file_patterns = [file_patterns]

    files = []
    for pattern in file_patterns:
        files.extend(glob.glob(os.path.join(directory_path, pattern), recursive=recursive))

    return files


def read_textfile(textfile, mode='lines', encoding='utf-8'):
    """
    Reads a textfile.
    :param textfile: The textfile path.
    :param mode: Determines the return type. 'lines' for a list of textfile lines or 'text' for one string containing
    all file content.
    :param encoding: The encoding of the textfile.
    :return: The content of the textfile.
    """
    f = open(textfile, 'r', encoding=encoding)
    if mode == 'lines':
        text = f.readlines()
    elif mode == 'text':
        text = f.read()
    else:
        raise NotImplementedError('The given mode {} is not implemented!'.format(mode))
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


def download_and_extract_zip_from_url(url, save_path):
    os.makedirs(save_path, exist_ok=True)
    url_request = requests.get(url, stream=True)
    zip_file = zipfile.ZipFile(BytesIO(url_request.content))
    zip_file.extractall(path=save_path)


def get_word_blacklist_regex(blacklist_file):
    word_blacklist = read_textfile(blacklist_file)
    word_blacklist = [line[:-1].lower() for line in word_blacklist]
    word_blacklist = set(word_blacklist)
    word_regex = '|'.join(word_blacklist)
    regex = r'(?i)\b({})\b'.format(word_regex)
    regex = re.compile(regex)

    return regex
