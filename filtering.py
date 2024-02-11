from scipy.signal import welch, butter, filtfilt
import numpy as np
import serial

ser = serial.Serial('COM5', 115200)

# Define threshold and window size
threshold = 28
window_size = 1000

# Initialize empty lists to store EMG data
emg1 = []
emg2 = []
emg3 = []
emg4 = []

# Initialize empty lists to store segmented EMG data
segments1 = []
segments2 = []
segments3 = []
segments4 = []

flag = 0
f = 1
i = 0
feature_matrix = np.empty((0, 16))

# Loop indefinitely
while True:
    try:
        data = ser.readline().strip().decode()
        print(data)
        channel1, channel2, channel3, channel4 = map(int, data.split(','))
        if f == 1:
            if channel1 > threshold or channel2 > threshold or channel3 > threshold or channel4 > threshold:
                emg1.append(channel1)
                emg2.append(channel2)
                flag = 1
                f = 0

        if flag == 1:
            emg1.append(channel1)
            emg2.append(channel2)
            i = i + 1
            if i == window_size:
                flag = 0
                f = 1
                i = 0
        # Add data to EMG data lists

        if len(emg1) >= window_size:
            # Get current window of EMG data for both channels
            window1 = emg1[-window_size:]
            window2 = emg2[-window_size:]

            # Extracting handcrafted features
            # rms
            rmsValue1 = np.sqrt(np.mean(np.square(window1)))
            rmsValue2 = np.sqrt(np.mean(np.square(window2)))

            # mav
            mav_feature_1 = np.mean(np.abs(window1))
            mav_feature_2 = np.mean(np.abs(window2))

            # zc
            zc_feature_1 = np.sum(np.abs(np.diff(np.sign(window1)))) / (2 * len(window1))
            zc_feature_2 = np.sum(np.abs(np.diff(np.sign(window2)))) / (2 * len(window2))

            # waveform length
            wl_feature_1 = np.sum(np.abs(np.diff(window1)))
            wl_feature_2 = np.sum(np.abs(np.diff(window2)))

            # ssc
            ssc_feature_1 = np.sum(np.abs(np.diff(np.sign(np.diff(window1))))) / (2 * len(window1))
            ssc_feature_2 = np.sum(np.abs(np.diff(np.sign(np.diff(window2))))) / (2 * len(window2))

            # mav slope
            mav_slope_feature_1 = np.mean(np.abs(np.diff(window1)))
            mav_slope_feature_2 = np.mean(np.abs(np.diff(window2)))

            # ar coeff

            ar_order = 4
            ar_coeffs1 = np.zeros(ar_order)
            ar_coeffs2 = np.zeros(ar_order)
            for j in range(ar_order):
                ar_coeffs1[j] = np.polyfit(window1[:-j - 1], window1[j + 1:], deg=1)[0]
                ar_coeffs2[j] = np.polyfit(window2[:-j - 1], window2[j + 1:], deg=1)[0]

            # psd
            freqs1, psd1 = welch(window1)
            freqs2, psd2 = welch(window2)
            psd_max_index1 = np.argmax(psd1)
            psd_max_index2 = np.argmax(psd2)
            psd_max_freq1 = freqs1[psd_max_index1]
            psd_max_freq2 = freqs2[psd_max_index2]

            # add to a matrix
            feature_matrix = np.vstack((feature_matrix,
                                        [mav_feature_1, rmsValue1, zc_feature_1, wl_feature_1, ssc_feature_1,
                                         mav_slope_feature_1, ar_coeffs1[0], psd_max_freq1, mav_feature_2,
                                         rmsValue2, zc_feature_2, wl_feature_2, ssc_feature_2, mav_slope_feature_2,
                                         ar_coeffs2[0], psd_max_freq2]))

    except ValueError:
        print(f"Skipping invalid data: {data}")

    # Clear segmented EMG data lists if they exceed a certain length
    if len(segments1) > 100:
        segments1 = []
    if len(segments2) > 100:
        segments2 = []