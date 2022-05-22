import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import accuracy_score

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


def detect_diabetes(pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree_function, age):
    # Loading the diabetes dataset to a pandas DataFrame
    diabetes_dataset = pd.read_csv(APP_ROOT + '/diabetes_data.csv')

    # Separating the data and labels
    X = diabetes_dataset.drop(columns='Outcome', axis=1)
    Y = diabetes_dataset['Outcome']

    # Data standardization
    scaler = StandardScaler()
    scaler.fit(X)
    standardized_data = scaler.transform(X)

    X = standardized_data
    Y = diabetes_dataset['Outcome']

    # Train and test split
    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y, test_size=0.2, stratify=Y, random_state=2)

    # Training the model
    classifier = svm.SVC(kernel='linear')

    # Training the support vector machine classifier
    classifier.fit(X_train, Y_train)

    # Model evaluation and accuracy score

    # Accuracy score on the training data
    X_train_prediction = classifier.predict(X_train)
    training_data_accuracy = accuracy_score(X_train_prediction, Y_train)
    print('Training data accuracy score : ', training_data_accuracy)

    # accuracy score on the test data
    X_test_prediction = classifier.predict(X_test)
    test_data_accuracy = accuracy_score(X_test_prediction, Y_test)
    print('Test data accuracy score : ', test_data_accuracy)

    # Making a predictive
    # input_data = (5, 166, 72, 19, 175, 25.8, 0.587, 51)
    input_data = (pregnancies, glucose, blood_pressure,
                  skin_thickness, insulin, bmi, diabetes_pedigree_function, age)

    # Changing the input_data to numpy array
    input_data_as_numpy_array = np.asarray(input_data)

    # Reshape the array as we are predicting for one instance
    input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)

    # Standardize the input data
    std_data = scaler.transform(input_data_reshaped)

    # Get prediction
    prediction = classifier.predict(std_data)
    print(prediction)

    if (prediction[0] == 0):
        return "The person is not diabetic"
    else:
        return "The person is diabetic"


# if __name__ == "__main__":
#     prediction = detect_diabetes(5, 166, 72, 19, 175, 25.8, 0.587, 51)
#     print(f"{prediction}")
