from scr.main.loading_dataset import load_signals
import matplotlib.pyplot as plt
from scr.main.preprocessing import pre_process
from scr.main.segmentation import segment

if __name__ == '__main__':
    # Create the data loader and load the first sample
    data_loader = load_signals()
    #next(data_loader)
    #next(data_loader)
    #next(data_loader)
    #next(data_loader)
    #next(data_loader)

    file_path, sample_rate, signal, signal_duration = next(data_loader)

    sample_rate, normalized_shannon_energy = pre_process(sample_rate, signal)
    filtered_signal, s1_peaks, s2_peaks = segment(normalized_shannon_energy, sample_rate)

    plt.figure("find peaks")

    filtered_plot = plt.subplot(211)
    filtered_plot.set_title("Signal after segmentation")
    filtered_plot.plot(filtered_signal)
    filtered_plot.set_xlabel("time [ms]")
    filtered_plot.set_ylabel('energy')

    file_name = file_path.split('/')[-1]
    print('filePath: ', file_path)
    print('fileName: ', file_name, '\n')
    sig_plot = plt.subplot(212)
    sig_plot.set_title("Signal with S1 & S2 peaks")
    sig_plot.plot(normalized_shannon_energy)
    sig_plot.plot(s1_peaks, normalized_shannon_energy[s1_peaks], "x", label='S1 peaks')
    sig_plot.plot(s2_peaks, normalized_shannon_energy[s2_peaks], "x", label='S2 peaks')
    sig_plot.set_xlabel("time [ms]")
    sig_plot.set_ylabel('energy')
    sig_plot.legend(loc='upper right')

    plt.show()
