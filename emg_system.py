import numpy as np

WINDOW_SIZE = 150
NUM_OF_SENSORS = 4
OVERLAP = int(WINDOW_SIZE / 2)
THRESHOLD = 560

c = 0
first = True

emg_1 = np.zeros((NUM_OF_SENSORS, WINDOW_SIZE))

while True:
    emg_1[0, c] = np.random.uniform(5, 10)
    emg_1[1, c] = np.random.uniform(5, 10)
    emg_1[2, c] = np.random.uniform(5, 10)
    emg_1[3, c] = np.random.uniform(5, 10)

    if (c == WINDOW_SIZE - 1 and first) or (c == OVERLAP + 1 and not first):
        print(f'Arr = {emg_1}')
        c = OVERLAP
        first = False

        emg_1 = np.roll(emg_1, OVERLAP, axis=1)
        wl = np.sum(np.abs(np.abs(emg_1[0, :])))

        if wl > THRESHOLD:
            x = np.array([])

            for row in emg_1:
                v = np.sqrt(np.mean(row ** 2)), np.mean(abs(row)), np.sum(row ** 2), np.sum(abs(row))
                v = list(v)
                x = np.hstack((x, np.array(v)))

            # prediction = model(X)

    else:
        c = c + 1



