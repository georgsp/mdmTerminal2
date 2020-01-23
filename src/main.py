#!/usr/bin/env python3

import os
import signal
import sys
import tempfile
from copy import deepcopy

from default_settings import CFG
from loader import Loader
from utils import SignalHandler

HOME = os.path.abspath(sys.path[0])


def get_cfg():
    return deepcopy(CFG)


def get_path(home) -> dict:
    path = {
        'home': home,
        # Расширение моделей
        'model_ext': '.pmdl',
        # Поддерживаемые модели
        'model_supports': ['.pmdl', '.umdl'],
        # Временные файлы
        'tmp': tempfile.gettempdir(),
        # ~/settings.ini
        'settings': os.path.join(home, 'settings.ini'),
        # ~/resources/
        'resources': os.path.join(home, 'resources'),
        # ~/data/
        'data': os.path.join(home, 'data'),
        # ~/plugins/
        'plugins': os.path.join(home, 'plugins'),
        # ~/test/
        'test': os.path.join(home, 'test'),
        # Раширение тестовых файлов
        'test_ext': '.wav',
    }
    path['models'] = os.path.join(path['resources'], 'models')
    path['samples'] = os.path.join(path['resources'], 'samples')
    # ~/resources/ding.wav ~/resources/dong.wav ~/resources/tts_error.mp3
    audio = (('ding', 'ding.wav'), ('dong', 'dong.wav'), ('bimp', 'bimp.mp3'), ('tts_error', 'tts_error.mp3'))
    for (key, val) in audio:
        path[key] = os.path.join(path['resources'], val)
    return path


def main():
    print('MAIN: Start...')
    sig = SignalHandler((signal.SIGINT, signal.SIGTERM))
    loader = Loader(init_cfg=get_cfg(), path=get_path(HOME), die_in=sig.die_in)
    try:
        loader.start_all_systems()
    except RuntimeError:
        pass
    else:
        sig.sleep(None)
    loader.stop_all_systems()
    print('MAIN: bye.')
    return loader.reload


if __name__ == '__main__':
    while main():
        pass
