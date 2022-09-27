from scipy.signal import cheby1, sosfilt
import numpy as np


def pre_process(sample_rate, signal):
    # Apply Chebyshev low pass filter
    ##### Cheby filter doesn't alter the signal much, this can be replaced by any other low pass filter
    f_cut = 882  # Hz
    f_sampling = sample_rate  # The sample rate in the paper is around 2000 which is equal to what we have so no resampling
    wn = f_cut / (0.5 * f_sampling)
    sos = cheby1(8, 1, wn, output='sos')  # The ripple factor (the second argument) was not mentioned in the paper
    filtered_signal = sosfilt(sos, signal)

    # Normalize the signal
    max_abs_value = np.max(np.abs(filtered_signal))
    normalized_signal = filtered_signal / max_abs_value

    # Calculate the envelope using Shannon energy
    envelope = normalized_signal ** 2 * np.log(normalized_signal ** 2)

    # Calculate the average Shannon energy
    # Note: average Shannon energy resample the signal with 100 Hz frequency
    # (because of 0.01-second shift) of the averaging window)
    new_sample_rate = 100
    shift = int(0.01 * sample_rate)  # The number of samples in a 0.01-second window
    window_width = shift * 2
    average_shannon_energy = []
    for i in range((len(envelope) - shift) // shift):
        average_shannon_energy.append(-1 * np.mean(envelope[i * shift:i * shift + window_width]))
    average_shannon_energy = np.array(average_shannon_energy)

    # Normalize the average Shannon energy
    normalized_shannon_energy = (average_shannon_energy - np.mean(average_shannon_energy)) / np.std(
        average_shannon_energy)

    return new_sample_rate, normalized_shannon_energy
