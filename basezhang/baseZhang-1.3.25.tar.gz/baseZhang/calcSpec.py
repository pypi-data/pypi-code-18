import pylab
from scipy.io import wavfile


def get_wav_info(wav_file):
    rate, data = wavfile.read(wav_file)
    return rate, data


def get_spec(wavPath):
    frame_rate, sound_info = get_wav_info(wavPath)
    print frame_rate
    Pxx, freqs, bins, im = pylab.specgram(sound_info, Fs=frame_rate)
    return Pxx

