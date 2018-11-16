
import hashlib
import json
import time
from io import BytesIO

import requests
from bs4 import BeautifulSoup
from speech_recognition import AudioData

from utils import REQUEST_ERRORS
from .proxy import proxies

__all__ = ['Yandex', 'PocketSphinxREST']


class UnknownValueError(Exception):
    pass


class BaseSTT:
    BUFF_SIZE = 1024

    def __init__(self, url, audio_data: AudioData,
                 headers=None, convert_rate=None, convert_width=None, proxy_key=None, **kwargs):
        self._text = None
        self._rq = None
        self._url = url
        self._convert_rate = convert_rate
        self._convert_width = convert_width
        self._audio = self._get_audio(audio_data)
        self._headers = {'Transfer-Encoding': 'chunked'}
        if isinstance(headers, dict):
            self._headers.update(headers)
        self._params = kwargs

        self._send(proxy_key)
        self._reply_check()
        self._parse_response()

    def _get_audio(self, audio_data: AudioData):
        return audio_data.get_wav_data(self._convert_rate, self._convert_width)

    def _chunks(self):
        with BytesIO(self._audio) as fp:
            while True:
                chunk = fp.read(self.BUFF_SIZE)
                yield chunk
                if not chunk:
                    break

    def _send(self, proxy_key):
        try:
            self._rq = requests.post(
                self._url,
                data=self._chunks(),
                params=self._params,
                headers=self._headers,
                stream=True,
                timeout=60,
                proxies=proxies(proxy_key)
            )
        except REQUEST_ERRORS as e:
            raise RuntimeError(str(e))

    def _reply_check(self):
        if not self._rq.ok:
            msg = BeautifulSoup(self._rq.text, features='html.parser').text.replace('\n', ' ')[:99]
            raise RuntimeError('{}: {}'.format(self._rq.status_code, msg))

    def _parse_response(self):
        pass

    def text(self):
        return self._text


class Yandex(BaseSTT):
    URL = 'https://asr.yandex.net/asr_xml'

    def __init__(self, audio_data: AudioData, key, lang='ru-RU'):
        # https://tech.yandex.ru/speechkit/cloud/doc/guide/common/speechkit-common-asr-http-request-docpage/
        if not key:
            raise RuntimeError('API-Key unset')
        rate = 16000
        width = 2
        headers = {'Content-Type': 'audio/x-pcm;bit={};rate={}'.format(width*8, rate)}
        kwargs = {
            'uuid': hashlib.sha1(str(time.time()).encode()).hexdigest()[:32],
            'key': key,
            'topic': 'queries',
            'lang': lang,
            'disableAntimat': 'true'
        }
        super().__init__(self.URL, audio_data, headers, rate, width, 'stt_yandex', **kwargs)

    def _get_audio(self, audio_data: AudioData):
        return audio_data.get_raw_data(self._convert_rate, self._convert_width)

    def _parse_response(self):
        self._text = xml_yandex(self._rq.text)


class PocketSphinxREST(BaseSTT):
    def __init__(self, audio_data: AudioData, url='http://127.0.0.1:8085'):
        url = '{}/stt'.format(url)
        super().__init__(url, audio_data, {'Content-Type': 'audio/wav'}, 16000, 2, 'stt_pocketsphinx-rest')

    def _parse_response(self):
        try:
            result = json.loads(''.join(self._rq.text.split('\n')))
        except (json.JSONDecodeError, ValueError, TypeError) as e:
            raise RuntimeError('Json decode error: {}'.format(e))

        if 'code' not in result or 'text' not in result or result['code']:
            raise RuntimeError('Response error: {}: {}'.format(result.get('code', 'None'), result.get('text', 'None')))
        self._text = result['text']
        if not self._text:
            raise UnknownValueError('No variants')


def xml_yandex(data):
    # https://tech.yandex.ru/speechkit/cloud/doc/guide/common/speechkit-common-asr-http-response-docpage/
    success_shift = 9
    variant_len = 10
    text = ''
    end_point = 0
    success_found = False
    for test in data.split('\n'):
        if success_found:
            end_point = test.rfind('</variant>')
            if end_point > 0:
                text = test
                break
        else:
            start_success = test.find('success="') + success_shift
            if start_success > success_shift:
                success_str = test[start_success:start_success+1]
                if success_str == '1':
                    success_found = True
                elif success_str == '0':
                    raise UnknownValueError('No variants')
                else:
                    raise RuntimeError('xml: root attribute broken - \'{}\''.format(success_str))

    if not success_found:
        raise RuntimeError('xml: root attribute not found, not XML?')

    start_variant = text.find('>') + 1
    if start_variant < variant_len or start_variant > end_point:
        raise RuntimeError('xml: broken XML')
    text = text[start_variant:end_point]
    if not text:
        raise RuntimeError('xml: get empty text, WTF?')
    return text
