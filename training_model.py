import os

import pandas as pd
import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from micromlgen import port

WINDOW_SIZE = 150
NUM_OF_SENSORS = 4
OVERLAP = int(WINDOW_SIZE / 2)
THRESHOLD = 560
ENTRIES_FOLDER = './entries_classification_3'


def extract_features_from_entry(values):
    n = np.array([])

    for row in values:
        v = np.sqrt(np.mean(row ** 2)), np.mean(abs(row)), np.sum(row ** 2), np.sum(abs(row))
        v = list(v)
        n = np.hstack((n, np.array(v)))

    return n


def get_feature_matrix():

    rows = []
    for filename in os.listdir(ENTRIES_FOLDER):
        print(filename)
        values = pd.read_csv(f'{ENTRIES_FOLDER}/{filename}').iloc[:, 1:]
        label = int(filename[0])

        c = 0
        first = True
        emg_raw = np.zeros((NUM_OF_SENSORS, WINDOW_SIZE))

        for _, row in values.iterrows():
            emg_raw[:, c] = row

            if (c == WINDOW_SIZE - 1 and first) or (c == OVERLAP + 1 and not first):
                c = OVERLAP
                first = False

                emg_raw = np.roll(emg_raw, OVERLAP, axis=1)
                wl = np.sum(np.abs(np.abs(emg_raw[0, :])))

                if wl > THRESHOLD:
                    row = list(extract_features_from_entry(emg_raw)) + [label]
                    rows.append(row)
            else:
                c = c + 1

        columns = ['RMS', 'MAV', 'SSI', 'IEMG']
        columns = [f"{item}_{i}" for i in range(1, NUM_OF_SENSORS + 1) for item in columns] + ['label']

    return pd.DataFrame(rows, columns=columns)


feature_matrix = get_feature_matrix()

print(feature_matrix)

X = feature_matrix.iloc[:, :-1].values
Y = feature_matrix['label'].values

encoder = LabelEncoder()
y = encoder.fit_transform(Y)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define the SVM model with your choice of hyperparameters
clf = svm.SVC(kernel='linear', C=0.1, gamma=0.1)

# Train the SVM model on the training set
clf.fit(X_train, y_train)

# Use the trained SVM model to predict on the testing set
y_pred = clf.predict(X_test)

# Evaluate the accuracy of the SVM model on the testing set
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

with open('SVMClassifier.h', 'w') as file:
    file.write(port(clf))

print('Finish')
