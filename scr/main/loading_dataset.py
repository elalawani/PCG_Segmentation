from glob import glob
from scipy.io import wavfile
import librosa


def load_signals(data_path='resources/training-a'):
    """A generator to load the signals one by one"""
    files_path = glob(data_path + '/*.wav')
    files_path.sort()

    for file_path in files_path:
        sample_rate, signal = wavfile.read(file_path)
        signal_duration = librosa.get_duration(filename=file_path)

        yield file_path, sample_rate, signal, signal_duration

    print(files_path)
