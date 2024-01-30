import time
import matplotlib.pyplot as plt
import numpy as np
import serial
import csv

ser = serial.Serial('COM4', 115200)  # Adjust the port and baud rate based on your setup
csv_file = open('emg_data.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)

num = 0

try:
    print('now')
    now = time.time()
    while num < 10_000:
        data = ser.readline().decode().strip()
        values = data.split(',')
        csv_writer.writerow(values)
        num += 1

    print(time.time() - now)

except KeyboardInterrupt:
    csv_file.close()
    ser.close()

csv_file.close()
ser.close()

data = np.genfromtxt('emg_data.csv', delimiter=',')

# Plot the data
plt.plot(data[:,0])
plt.xlabel('Sample')
plt.ylabel('EMG Value')
plt.title('EMG Data')
plt.show()