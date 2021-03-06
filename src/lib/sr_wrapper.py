# https://github.com/Uberi/speech_recognition
# Copyright (c) 2014-2017, Anthony Zhang <azhang9@gmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions
# and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions
# and the following disclaimer in the documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse
# or promote products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# This code was modified by Aculeasis, 2018

import audioop
import collections
import json
import math
import time

import speech_recognition

from .audio_utils import APMSettings, MicrophoneStreamAPM, MicrophoneStream, StreamRecognition, RMS, StreamDetector
from .proxy import proxies

AudioData = speech_recognition.AudioData
AudioSource = speech_recognition.AudioSource
UnknownValueError = speech_recognition.UnknownValueError
RequestError = speech_recognition.RequestError
WaitTimeoutError = speech_recognition.WaitTimeoutError
get_flac_converter = speech_recognition.get_flac_converter


class Interrupted(Exception):
    pass


class Microphone(speech_recognition.Microphone):
    DEFAULT_RATE = 16000

    def __init__(self, device_index=None, _=None, chunk_size=1024):
        super().__init__(device_index, self.DEFAULT_RATE, chunk_size)

    def __enter__(self):
        assert self.stream is None, "This audio source is already inside a context manager"
        self.audio = self.pyaudio_module.PyAudio()
        try:
            self.stream = Microphone.get_microphone_stream(
                self.audio.open(
                    input_device_index=self.device_index, channels=1,
                    format=self.format, rate=self.SAMPLE_RATE, frames_per_buffer=self.CHUNK,
                    input=True,  # stream is an input stream
                ), self.SAMPLE_WIDTH, self.SAMPLE_RATE
            )
        except Exception:
            self.audio.terminate()
            raise
        return self

    @classmethod
    def get_microphone_stream(cls, pyaudio_stream, width, rate):
        if APMSettings().enable:
            return MicrophoneStreamAPM(pyaudio_stream, width, rate, APMSettings().conservative)
        else:
            return MicrophoneStream(pyaudio_stream)

    @staticmethod
    def get_microphone_name(index=None):
        audio = Microphone.get_pyaudio().PyAudio()
        try:
            info = audio.get_default_input_device_info() if index is None else audio.get_device_info_by_index(index)
            return info['name']
        except (IOError, KeyError, TypeError) as e:
            return str(e)
        finally:
            audio.terminate()


class Recognizer(speech_recognition.Recognizer):
    def __init__(self, record_callback=None, silent_multiplier=1.0):
        super().__init__()
        self._record_callback = record_callback

        silent_multiplier = min(5.0, max(0.1, silent_multiplier))
        self.pause_threshold *= silent_multiplier
        self.non_speaking_duration = 0.8 * silent_multiplier

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def recognize_bing(self, audio_data, key, language="en-US", show_all=False):
        proxies.monkey_patching_enable('stt_microsoft')
        try:
            return super().recognize_bing(audio_data, key, language, show_all)
        finally:
            proxies.monkey_patching_disable()

    # part of https://github.com/Uberi/speech_recognition/blob/master/speech_recognition/__init__.py#L616
    def listen1(self, source, vad, timeout=None, phrase_time_limit=None, hw_buffer=None, hw_time=None):
        seconds_per_buffer = float(source.CHUNK) / source.SAMPLE_RATE
        # number of buffers of non-speaking audio during a phrase, before the phrase should be considered complete
        pause_buffer_count = int(math.ceil(self.pause_threshold / seconds_per_buffer))
        # minimum number of buffers of speaking audio before we consider the speaking audio a phrase
        phrase_buffer_count = int(math.ceil(self.phrase_threshold / seconds_per_buffer))
        # maximum number of buffers of non-speaking audio to retain before and after a phrase
        non_speaking_buffer_count = int(math.ceil(self.non_speaking_duration / seconds_per_buffer))

        # read audio input for phrases until there is a phrase that is long enough
        elapsed_time = 0  # number of seconds of audio read
        pause_count = 0
        buffer = b''  # an empty buffer means that the stream has ended and there is no data left to read
        send_record_starting = False
        # Use snowboy to words detecting instead of energy_threshold
        while True:
            frames = collections.deque()
            if hw_time is None:
                # store audio input until the phrase starts
                while True:
                    # handle waiting too long for phrase by raising an exception
                    elapsed_time += seconds_per_buffer
                    if timeout and elapsed_time > timeout:
                        if self._record_callback and send_record_starting:
                            self._record_callback(False)
                        raise WaitTimeoutError("listening timed out while waiting for phrase to start")

                    buffer = source.stream.read(source.CHUNK)
                    if not buffer:
                        break  # reached end of the stream
                    frames.append(buffer)
                    if len(frames) > non_speaking_buffer_count:
                        # ensure we only keep the needed amount of non-speaking buffers
                        frames.popleft()

                    # detect whether speaking has started on audio input
                    if vad.is_speech(buffer):
                        break
                    # dynamically adjust the energy threshold using asymmetric weighted average
                    vad.dynamic_energy()
            else:
                elapsed_time += hw_time
                if not hw_buffer:
                    break  # reached end of the stream
                frames.append(b''.join(hw_buffer))
                hw_buffer, hw_time = None, None

            # read audio input until the phrase ends
            pause_count, phrase_count = 0, 0
            phrase_start_time = elapsed_time
            if self._record_callback and not send_record_starting:
                send_record_starting = True
                self._record_callback(True)
            while True:
                # handle phrase being too long by cutting off the audio
                elapsed_time += seconds_per_buffer
                if phrase_time_limit and elapsed_time - phrase_start_time > phrase_time_limit:
                    break

                buffer = source.stream.read(source.CHUNK)
                if not buffer:
                    break  # reached end of the stream
                frames.append(buffer)
                phrase_count += 1

                # check if speaking has stopped for longer than the pause threshold on the audio input
                if vad.is_speech(buffer):
                    pause_count = 0
                else:
                    pause_count += 1
                if pause_count > pause_buffer_count:  # end of the phrase
                    break

            # check how long the detected phrase is, and retry listening if the phrase is too short
            phrase_count -= pause_count  # exclude the buffers for the pause before the phrase
            if phrase_count >= phrase_buffer_count or len(buffer) == 0:
                break  # phrase is long enough or we've reached the end of the stream, so stop listening

        # obtain frame data
        for i in range(pause_count - non_speaking_buffer_count):
            frames.pop()  # remove extra non-speaking frames at the end
        frame_data = b"".join(frames)
        if self._record_callback and send_record_starting:
            self._record_callback(False)
        return AudioData(frame_data, source.SAMPLE_RATE, source.SAMPLE_WIDTH)

    def listen2(self, source, vad, recognition, timeout, phrase_time_limit=None, hw_buffer=None, hw_time=None):
        timeout = timeout or 5
        seconds_per_buffer = float(source.CHUNK) / source.SAMPLE_RATE
        # number of buffers of non-speaking audio during a phrase, before the phrase should be considered complete
        pause_buffer_count = int(math.ceil(self.pause_threshold / seconds_per_buffer))
        # minimum number of buffers of speaking audio before we consider the speaking audio a phrase
        phrase_buffer_count = int(math.ceil(self.phrase_threshold / seconds_per_buffer))
        # maximum number of buffers of non-speaking audio to retain before and after a phrase
        non_speaking_buffer_count = int(math.ceil(self.non_speaking_duration / seconds_per_buffer))

        # read audio input for phrases until there is a phrase that is long enough
        elapsed_time = 0  # number of seconds of audio read
        buffer = b''  # an empty buffer means that the stream has ended and there is no data left to read
        # Use snowboy to words detecting instead of energy_threshold
        send_record_starting = False
        voice_recognition = StreamRecognition(recognition)
        while voice_recognition.processing:
            if hw_time is None:
                # store audio input until the phrase starts
                silent_frames = collections.deque(maxlen=non_speaking_buffer_count)
                while voice_recognition.processing:
                    # handle waiting too long for phrase by raising an exception
                    elapsed_time += seconds_per_buffer
                    if timeout and elapsed_time > timeout:
                        if self._record_callback and send_record_starting:
                            self._record_callback(False)
                        voice_recognition.terminate()
                        raise WaitTimeoutError("listening timed out while waiting for phrase to start")

                    buffer = source.stream.read(source.CHUNK)
                    if not buffer:
                        break  # reached end of the stream

                    # detect whether speaking has started on audio input
                    silent_frames.append(buffer)
                    if vad.is_speech(buffer):
                        if voice_recognition.ready:
                            voice_recognition.write(b''.join(silent_frames))
                        else:
                            voice_recognition.init(silent_frames, None, source.SAMPLE_RATE, source.SAMPLE_WIDTH)
                        break
                    # dynamically adjust the energy threshold using asymmetric weighted average
                    vad.dynamic_energy()
            else:
                elapsed_time += hw_time
                if not hw_buffer:
                    break  # reached end of the stream
                voice_recognition.init(hw_buffer, None, source.SAMPLE_RATE, source.SAMPLE_WIDTH)
                hw_buffer, hw_time = None, None

            # read audio input until the phrase ends
            pause_count, phrase_count = 0, 0
            phrase_start_time = elapsed_time
            if self._record_callback and not send_record_starting:
                send_record_starting = True
                self._record_callback(True)
            while voice_recognition.processing:
                # 100% frames must be available for call read()
                if not source.stream.read_available:
                    time.sleep(0.004)
                    continue
                buffer = source.stream.read(source.CHUNK)
                if not buffer:
                    # reached end of the stream
                    break

                # handle phrase being too long by cutting off the audio
                elapsed_time += seconds_per_buffer
                if phrase_time_limit and elapsed_time - phrase_start_time >= phrase_time_limit:
                    break

                voice_recognition.write(buffer)
                phrase_count += 1

                if vad.is_speech(buffer):
                    pause_count = 0
                else:
                    pause_count += 1
                if pause_count > pause_buffer_count:  # end of the phrase
                    break

            # check how long the detected phrase is, and retry listening if the phrase is too short
            phrase_count -= pause_count  # exclude the buffers for the pause before the phrase
            if phrase_count >= phrase_buffer_count or len(buffer) == 0:
                break  # phrase is long enough or we've reached the end of the stream, so stop listening

        if self._record_callback and send_record_starting:
            self._record_callback(False)

        voice_recognition.end()
        if voice_recognition.ready:
            if not voice_recognition.is_ok:
                voice_recognition.work = False
                raise RuntimeError('None')
        else:
            voice_recognition.work = False
            raise RuntimeError('None')
        return voice_recognition

    def listen3(self, source, stream_hwd: StreamDetector, phrase_time_limit):
        seconds_per_buffer = float(source.CHUNK) / source.SAMPLE_RATE
        pause_buffer_count = int(math.ceil(self.pause_threshold / seconds_per_buffer))

        pause_count, elapsed_time = 0, 0
        self._record_callback and self._record_callback(True)
        try:
            while stream_hwd.processing:
                if not source.stream.read_available:
                    time.sleep(0.004)
                    continue
                buffer = source.stream.read(source.CHUNK)
                if not buffer:
                    break

                elapsed_time += seconds_per_buffer
                if phrase_time_limit and elapsed_time >= phrase_time_limit:
                    break

                if stream_hwd.is_speech(buffer):
                    pause_count = 0
                else:
                    pause_count += 1
                if pause_count > pause_buffer_count:
                    break
        finally:
            self._record_callback and self._record_callback(False)
        stream_hwd.end()

        if not stream_hwd.is_ok:
            raise RuntimeError('None')
        return stream_hwd


class EnergyDetectorVAD:
    WRONG_RMS = 32768

    def __init__(self, source, width, rate, energy_lvl, energy_dynamic, rms, **_):
        self.dynamic_energy_adjustment_damping = 0.15
        self.dynamic_energy_ratio = 1.5
        self._width = width
        self._dynamic_energy_threshold = energy_dynamic
        self._chunk_size = float(source.CHUNK)
        self._seconds_per_buffer = None
        self._rms = RMS(width) if rms else None
        self.set_rate(rate)
        if not energy_lvl:
            self._energy_threshold = 500
            self._energy = None
        else:
            self._energy_threshold = energy_lvl
            self._energy = energy_lvl
            self._dynamic_energy()

    @property
    def energy_threshold(self):
        return int(self._energy_threshold)

    def set_rate(self, rate: int):
        self._seconds_per_buffer = self._chunk_size / rate

    def force_adjust_for_ambient_noise(self, source):
        if self._energy is None:
            stream = source.stream
            try:
                stream or source.__enter__()
                self.adjust_for_ambient_noise(source.stream, source.CHUNK)
            finally:
                stream or source.__exit__(None, None, None)

    def adjust_for_ambient_noise(self, stream, chunk, duration=1):
        elapsed_time = 0
        while True:
            elapsed_time += self._seconds_per_buffer
            if elapsed_time > duration:
                break
            buffer = stream.read(chunk)
            if not buffer:
                break
            # energy of the audio signal
            energy = audioop.rms(buffer,  self._width)
            if energy != self.WRONG_RMS:
                self._energy = energy
                self._dynamic_energy()

    def is_speech(self, buffer: bytes) -> bool:
        energy = audioop.rms(buffer,  self._width)
        if energy == self.WRONG_RMS:
            return False
        self._rms and self._rms.calc(energy)
        result = energy > self._energy_threshold
        self._energy = None if result else energy
        return result

    def rms(self) -> tuple or None:
        return self._rms.result() if self._rms else None

    def dynamic_energy(self):
        if self._energy is not None and self._dynamic_energy_threshold:
            self._dynamic_energy()

    def _dynamic_energy(self):
        damping = self.dynamic_energy_adjustment_damping ** self._seconds_per_buffer
        target_energy = self._energy * self.dynamic_energy_ratio
        self._energy_threshold = self._energy_threshold * damping + target_energy * (1 - damping)


# part of https://github.com/Uberi/speech_recognition/blob/master/speech_recognition/__init__.py#L574
def wait_detection(source, snowboy, interrupt_check, noising=None, timeout=180):
    elapsed_time = 0
    seconds_per_buffer = float(source.CHUNK) / source.SAMPLE_RATE
    # buffers capable of holding 3 seconds of original and resampled audio
    five_seconds_buffer_count = int(math.ceil(3 / seconds_per_buffer))
    frames = collections.deque(maxlen=five_seconds_buffer_count)
    start_time = time.time() + 0.2
    snowboy_result = 0
    source.stream.deactivate()
    while True:
        elapsed_time += seconds_per_buffer

        buffer = source.stream.read(source.CHUNK)
        if not buffer:
            break  # reached end of the stream
        frames.append(buffer)
        snowboy_result = snowboy.detect(buffer)
        if snowboy_result > 0:
            # wake word found
            break
        elif snowboy_result == -1:
            raise RuntimeError("Error initializing streams or reading audio data")

        if time.time() > start_time:
            if interrupt_check():
                raise Interrupted('Interrupted')
            if elapsed_time > timeout:
                raise Interrupted("listening timed out while waiting for hotword to be said")
            start_time = time.time() + 0.2

        if noising and not noising():
            snowboy.dynamic_energy()
    return snowboy_result, source.stream.reactivate(frames), elapsed_time if elapsed_time < 5 else 5.0


def google_reply_parser(text: str) -> str:
    # ignore any blank blocks
    actual_result = None
    for line in text.split('\n'):
        if not line:
            continue
        try:
            result = json.loads(line).get('result', [])
        except json.JSONDecodeError:
            continue
        if result and isinstance(result[0], dict):
            actual_result = result[0].get('alternative')
            break

    # print(actual_result)
    if not actual_result:
        raise UnknownValueError()

    if 'confidence' in actual_result:
        # return alternative with highest confidence score
        return max(actual_result, key=lambda alternative: alternative['confidence']).get('transcript')
    else:
        # when there is no confidence available, we arbitrarily choose the first hypothesis.
        return actual_result[0].get('transcript')
