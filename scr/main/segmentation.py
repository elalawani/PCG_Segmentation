import copy
import numpy as np
from scipy.signal import argrelextrema


def segment(preprocessed_signal, sample_rate):
    # Apply the threshold
    threshold = 1
    filtered_signal = copy.deepcopy(preprocessed_signal)
    filtered_signal[filtered_signal < threshold] = threshold

    # Find local maxima
    local_maxima_ind = argrelextrema(filtered_signal, np.greater)
    mask = np.ones(preprocessed_signal.shape, bool)
    mask[local_maxima_ind] = False
    filtered_signal[mask] = threshold

    # Omit peaks that are too close
    sliding_window_width = 0.15  # seconds
    sliding_window = int(sliding_window_width * sample_rate)
    for i_start in range(len(filtered_signal) - sliding_window):
        cropped_signal = filtered_signal[i_start:i_start + sliding_window]
        mask = np.ones(cropped_signal.shape, bool)
        mask[cropped_signal.argmax()] = False
        cropped_signal[mask] = threshold
        filtered_signal[i_start:i_start + sliding_window] = cropped_signal

    # Find the most frequent intervals within a time window,
    # and we assume that that is S1-S2 as systolic period is the most constant
    peaks = np.where(filtered_signal > threshold)[0]
    intervals = np.diff(peaks) / sample_rate
    interval_frequency_window = 0.15  # seconds
    start = intervals.min() - 0.001  # to make sure that intervals min is caught in the loop below
    interval_frequency = []
    while start < intervals.max():
        interval_frequency.append([start, len(
            np.where(np.logical_and(intervals >= start, intervals < start + interval_frequency_window))[0])])
        start += 0.01
    interval_frequency = np.array(interval_frequency)
    most_frequent_interval = interval_frequency[interval_frequency[:, 1].argmax(), :]

    # find the s1 and s2 peaks indices on the filtered signal
    s1_peaks = peaks[np.where(np.logical_and(intervals >= most_frequent_interval[0],
                                             intervals < most_frequent_interval[0] + interval_frequency_window))[0]]
    s2_peaks = peaks[np.where(np.logical_and(intervals >= most_frequent_interval[0],
                                             intervals < most_frequent_interval[0] + interval_frequency_window))[0] + 1]

    # print("S1 peaks: ", s1_peaks)
    # print("S2 peaks: ", s2_peaks)

    return filtered_signal, s1_peaks, s2_peaks
