# coding=utf-8
import codecs
import json
import os
from threading import Thread

from audio_identify.analyzer import Analyzer
from audio_identify.collector import Collector
from audio_identify.emit.emiter import observer
from audio_identify.wav_player import Player
from common.conf_paser import parse_wav
from obj.default_json_decoder import DefaultDecoder
from common.logger import logger
from common.serial_util import get_com_devices
from common.time_util import format_time
from conf.config import CorpusConf
from obj.default_log_obj import write_default_log_2_csv


class AudioIdentify:
    def __init__(self):
        self.player = Player()
        self.com_devices = get_com_devices()
        self.collectors = []
        self.analyzers = []
        self.wav_mapping = parse_wav()
        self.w_thread = None
        self.can_write = True
        self.__init_default()

    def __init_default(self):
        self.register_collector_by_com()
        self.register_analyzer(Analyzer())
        self.start_write_result_thread()

    def start_write_result_thread(self, f=write_default_log_2_csv):
        self.w_thread = Thread(target=f, args=(self,))
        self.w_thread.start()

    def register_collector(self, c):
        """
        :type c: audio_identify.collector.Collector
        """
        if isinstance(c, Collector):
            c.start()
            self.collectors.append(c)
        else:
            logger.warn('invalid collector..., c:{0}'.format(c))

    def remove_collector(self, c):
        """
        :type c: audio_identify.collector.Collector
        """
        if isinstance(c, Collector):
            c.remove()
            observer.remove(c)
            self.collectors.remove(c)
        else:
            logger.warn('invalid collector..., c:{0}'.format(c))

    def register_collector_by_com(self):
        for device in self.com_devices:
            self.register_collector(Collector(device))

    def replace_collectors_by_com(self, com_l):
        """
        修改串口后，更新设置日志收集器
        :param com_l: 新的串口列表
        """
        for collector in self.collectors:
            self.remove_collector(collector)
        for com in com_l:
            self.register_collector(Collector(com))

    def register_analyzer(self, a):
        """
        :type a: audio_identify.collector.Analyzer
        """
        if isinstance(a, Analyzer):
            a.start()
            self.analyzers.append(a)
        else:
            logger.warn('invalid analyzer..., Analyzer::{0}'.format(a))

    def remove_analyzer(self, a):
        """
        :type a: audio_identify.collector.Analyzer
        """
        if isinstance(a, Analyzer):
            a.remove()
            self.analyzers.remove(a)
        else:
            logger.warn('invalid analyzer..., Analyzer::{0}'.format(a))

    def release(self):
        for collector in self.collectors:
            collector.remove()
        for analyzer in self.analyzers:
            analyzer.remove()
        self.can_write = False
        logger.info('test finish!!!!!!')

    def process(self):
        try:
            self.player.play_all(self.wav_mapping)
            self.release()
        except Exception as e:
            logger.error('error happen: %s' % e)

    def output_wav_text(self):
        file_name = 'test_wav_%s.json' % format_time(time_formatter="%Y%m%d%H%M%S")
        with codecs.open(os.path.join(CorpusConf.OUTPUT_PATH, file_name), 'w+', encoding='utf-8') as wf:
            json.dump(self.wav_mapping, wf, cls=DefaultDecoder, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    ai = AudioIdentify()
    ai.process()
