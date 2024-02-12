import os

import pandas as pd
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

def extract_features_from_entry(values):
    return sum(values), 2

def get_feature_matrix():

    rows = []
    for filename in os.listdir('./entries'):
        values = pd.read_csv(f'./entries/{filename}').iloc[:,1]
        label = int(filename[0])
        row = list(extract_features_from_entry(values)) + [label]
        rows.append(row)

    return pd.DataFrame(rows, columns=['sum', '1', 'label'])

feature_matrix = get_feature_matrix()

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
import joblib
# Save the trained SVM model
joblib.dump(clf, 'svm_model.joblib')

# Save the LabelEncoder
joblib.dump(encoder, 'label_encoder.joblib')
