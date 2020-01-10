# coding=utf-8


class CorpusConf:
    REMOTE_BASE = r'\\192.168.1.8'
    BASE_PATH = r'\corpus\project\mddc'  # 项目路径
    CMD_PATH = r'/res/config.json'
    WAV_MAPPING = {
        'scp': 'train_mini/wav.scp',
        'text': 'train_mini/text'
    }
    WAV_COUNT_ONE_CMDER = 2
    PLAY_SEPARATOR = 5  # 语音播报间隔
    LOG_FILTER = ['agc handler']  # 过滤掉包含关键字的日志
