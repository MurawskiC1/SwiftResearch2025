import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle

# Train a Random Forest classifier and save the model
def train_model():
    # Load the data
    data = pd.read_csv("processed_images.csv")

    # Use only the '99%_Verify' category and exclude rows with None labels

    data = data[data['99%_Verify'].notna()]
    labels = data['99%_Verify']
    features = data.drop(['Prop_Verify', '95%_Verify', '99%_Verify', 'png_path', 'Burst_Name'], axis=1).values

    print("Label counts before splitting:")
    print(labels.value_counts())
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        features, labels, test_size=0.20, stratify=labels, random_state=42
    )

    # Train the classifier
    classifier = RandomForestClassifier(random_state=42)
    classifier.fit(X_train, y_train)

    # Evaluate the model
    y_pred = classifier.predict(X_test)
    train_pred = classifier.predict(X_train)
    print(labels)
    print("Test Accuracy:", accuracy_score(y_test, y_pred))
    print("Train Accuracy:", accuracy_score(y_train, train_pred))

    # Save the trained model
    with open("random_forest_model.pkl", "wb") as f:
        pickle.dump(classifier, f)
    print("Model saved to random_forest_model.pkl")

if __name__ == "__main__":
    train_model()
