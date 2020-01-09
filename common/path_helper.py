# coding=utf-8
import os
import re

from conf.config import CorpusConf


def combine_path(base, *path1):
    r = base
    for p in path1:
        r = os.path.join(r, *re.split(r'[/\\]', p))
    return r


def get_cmder_path():
    return combine_path(CorpusConf.REMOTE_BASE, CorpusConf.BASE_PATH, CorpusConf.CMD_PATH)


def get_wav_scp_path():
    return combine_path(CorpusConf.REMOTE_BASE, CorpusConf.BASE_PATH, CorpusConf.WAV_MAPPING.get('scp'))


def get_wav_text_path():
    return combine_path(CorpusConf.REMOTE_BASE, CorpusConf.BASE_PATH, CorpusConf.WAV_MAPPING.get('text'))


if __name__ == '__main__':
    print(combine_path(CorpusConf.REMOTE_BASE, CorpusConf.BASE_PATH, CorpusConf.CMD_PATH))
