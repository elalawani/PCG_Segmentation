from scr.main.loading_dataset import load_signals
import matplotlib.pyplot as plt
from scr.main.preprocessing import pre_process

if __name__ == '__main__':
    # Create the data loader and load the first sample
    ##### This should go in for loop like for file_path, sample_rate, signal, signal_duration in data_loader:
    #### to work over all samples
    data_loader = load_signals()
    file_path, sample_rate, signal, signal_duration = next(data_loader)
    plt.figure("pre-processing phase")

    # Run some tests and plot the data
    file_name = file_path.split('/')[-1]
    print('filePath: ', file_path)
    print('fileName: ', file_name, '\n')
    sig_plot = plt.subplot(211)
    sig_plot.set_title("original Signal")
    sig_plot.plot(signal)
    sig_plot.set_xlabel('time [ms]')
    sig_plot.set_ylabel('amplitude')


    # pre-process and plot the data
    _, normalized_shannon_energy = pre_process(sample_rate, signal)
    filtered_plot = plt.subplot(212)
    filtered_plot.set_title("Signal after preprocessing")
    filtered_plot.plot(normalized_shannon_energy)
    filtered_plot.set_xlabel("time [ms]")
    filtered_plot.set_ylabel('energy')
    plt.show()
