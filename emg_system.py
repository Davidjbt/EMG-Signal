import numpy as np

WINDOW_SIZE = 10
NUM_OF_SENSORS = 4
OVERLAP = int(WINDOW_SIZE / 2)

c = 0
first = True

emg_1 = np.zeros((NUM_OF_SENSORS, WINDOW_SIZE))

while True:
    emg_1[0, c] = np.random.uniform(5, 10)
    emg_1[1:, c] = np.random.uniform(5, 10)
    emg_1[2:, c] = np.random.uniform(5, 10)
    emg_1[3:, c] = np.random.uniform(5, 10)

    if (c == WINDOW_SIZE - 1 and first) or (c == OVERLAP + 1 and not first):
        print(f'Arr = {emg_1}')
        c = OVERLAP
        first = False
        emg_1 = np.roll(emg_1, OVERLAP, axis=1)



    else:
        c = c + 1



