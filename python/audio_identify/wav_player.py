# coding=utf-8
import os
import shutil
import wave
from time import sleep

import pyaudio
from pydub import AudioSegment

from audio_identify.emit.emiter import observer
from common.logger import logger
from conf.config import corpus_conf
from obj.audio_obj import AudioObj


class Player:
    def __init__(self):
        self.player = Player._Player()
        self.__is_play = True

    def play(self, o, cmd_str=''):
        while not self.__is_play:
            pass

        logger.info('play cmd:{0}, and wav:{1}'.format(cmd_str, o))
        if isinstance(o, AudioObj):
            audio_duration = len(AudioSegment.from_wav(o.source)) / 1000
            self.player.play_wav(o.source)
            logger.info('audio_duration:{0}'.format(audio_duration))
        else:
            logger.info('audio source may be error, type:{0}'.format(type(o)))
        sleep(corpus_conf.play_separator)
        observer.notify(o)

    def play_batch(self, o_list, cmd_str='', repeat_play_count=corpus_conf.repeat_play_count):
        while repeat_play_count > 0:
            for o in o_list:
                self.play(o, cmd_str)
            repeat_play_count -= 1

    def play_all(self, o_dict, repeat_play_count):
        """
        :type o_dict: dict
        :param o_dict: 命令词：音频列表
        :param repeat_play_count: 单条命令重复次数（每次的音频不一样，内容一样）
        :return:
        """
        for cmd_str, wav_list in o_dict.items():
            self.play_batch(wav_list, cmd_str, repeat_play_count)

    class _Player:
        @staticmethod
        def play_wav(wav_name):
            tmp_file_path = shutil.copy(wav_name, corpus_conf.temp_path)
            chunk = 1024
            p = pyaudio.PyAudio()
            wf = wave.open(tmp_file_path, 'rb')
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)

            data = wf.readframes(chunk)
            while data != b'':
                stream.write(data)
                data = wf.readframes(chunk)

            stream.stop_stream()
            stream.close()
            p.terminate()
            wf.close()
            os.remove(tmp_file_path)

    def set_play(self, bol):
        self.__is_play = bool(bol)

    def is_play(self):
        return self.__is_play


player = Player()
if __name__ == '__main__':
    player.play(r'\\192.168.1.8/corpus/train/wavs/A1001/A1001_4244.wav')
    player.play(AudioObj({'source': r'\\192.168.1.8/corpus/train/wavs/A1001/A1001_4244.wav'}))
