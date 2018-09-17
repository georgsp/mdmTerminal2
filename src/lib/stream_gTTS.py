
import gtts
import requests
import urllib3
# noinspection PyProtectedMember
from gtts.utils import _len
from six.moves import urllib


class gTTS(gtts.gTTS):
    def __init__(self, text, lang, *_, **__):
        super().__init__(text=text, lang=lang)

    def save(self, file_path, queue_=None):
        if file_path:
            with open(file_path, 'wb') as fp:
                self.write_to_fp(fp, queue_)
        else:
            # noinspection PyTypeChecker
            self.write_to_fp(None, queue_)
        if queue_:
            queue_.put_nowait(None)

    def write_to_fp(self, fp, queue_=None):
        # When disabling ssl verify in requests (for proxies and firewalls),
        # urllib3 prints an insecure warning on stdout. We disable that.
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        text_parts = self._tokenize(self.text)
        assert text_parts, 'No text to send to TTS API'
        for idx, part in enumerate(text_parts):
            try:
                # Calculate token
                part_tk = self.token.calculate_token(part)
            except requests.exceptions.RequestException as e:  # pragma: no cover
                raise gtts.gTTSError(
                    "Connection error during token calculation: %s" %
                    str(e))

            payload = {'ie': 'UTF-8',
                       'q': part,
                       'tl': self.lang,
                       'ttsspeed': self.speed,
                       'total': len(text_parts),
                       'idx': idx,
                       'client': 'tw-ob',
                       'textlen': _len(part),
                       'tk': part_tk}
            r = None
            try:
                # Request
                r = requests.get(self.GOOGLE_TTS_URL,
                                 params=payload,
                                 headers=self.GOOGLE_TTS_HEADERS,
                                 proxies=urllib.request.getproxies(),
                                 verify=False,
                                 stream=True)

                r.raise_for_status()
            except requests.exceptions.HTTPError:
                # Request successful, bad response
                raise gtts.gTTSError(tts=self, response=r)
            except requests.exceptions.RequestException as e:  # pragma: no cover
                # Request failed
                raise gtts.gTTSError(str(e))
            for chunk in r.iter_content(chunk_size=1024):
                if queue_:
                    queue_.put_nowait(chunk)
                if fp:
                    fp.write(chunk)
