from scr.main.loading_dataset import load_signals
import matplotlib.pyplot as plt
from scr.main.preprocessing import pre_process
from scr.main.segmentation import segment
import numpy as np

if __name__ == '__main__':

    data_loader = load_signals()

    file_path, sample_rate, signal, signal_duration = next(data_loader)

    sample_rate, normalized_shannon_energy = pre_process(sample_rate, signal)
    filtered_signal, s1_peaks, s2_peaks = segment(normalized_shannon_energy, sample_rate)

    s1_peaks = np.multiply(s1_peaks, 20)
    s2_peaks = np.multiply(s2_peaks, 20)

    s1_peaks_start = s1_peaks - 80
    s1_peaks_end = s1_peaks + 180

    s2_peaks_start = s2_peaks - 75
    s2_peaks_end = s2_peaks + 75

    print("S1 start: ", s1_peaks_start)
    print("S1 end: ", s1_peaks_end)
    print("S2 start: ", s2_peaks_start)
    print("S2 end: ", s2_peaks_end)

    file_name = file_path.split('/')[-1]
    print('filePath: ', file_path)
    print('fileName: ', file_name, '\n')
    plt.figure('the final result')

    plt.plot(signal[0:int(len(signal) / 3)])
    plt.title('Segmentation')
    plt.xlabel('time [ms]')
    plt.ylabel('amplitude')

    for i in range(0, int(len(s1_peaks_start) / 3)):
        plt.axvspan(s1_peaks_start[i], s1_peaks_end[i], color='r', alpha=0.5, label='S1' if i == 0 else "")

    for i in range(0, int(len(s2_peaks_start) / 3)):
        plt.axvspan(s2_peaks_start[i], s2_peaks_end[i], color='g', alpha=0.5, label='S2' if i == 0 else "")

    plt.legend(loc='upper right')

    plt.show()
