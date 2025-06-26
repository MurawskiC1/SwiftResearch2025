import os
import pandas as pd
from skimage.io import imread
from skimage.transform import resize
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.tree import export_text, plot_tree
import matplotlib.pyplot as plt

# Function to find the PNG file associated with a burst name
def find_png(name, path="BurstPhotos"):
    for filename in os.listdir(path):
        if name in filename and os.path.isfile(os.path.join(path, filename)):
            return os.path.join(path, filename)
    return None

# Function to process images and labels
def process_csv(file_path, img_size=(32, 32), path_to_images="BurstPhotos"):
    images = []
    labels = []
    png_paths = []
    all_images = []

    file = pd.read_csv(file_path)
    for _, row in file.iterrows():
        png_path = find_png(row['Burst_Name'], path_to_images)
        png_paths.append(png_path.split("/")[-1] if png_path else None)

        if png_path:  # Process only if a PNG exists
            try:
                img = imread(png_path)
                img = resize(img, img_size).flatten()  # Resize and flatten
                labelProp = row['99%_Verify']
                all_images.append(img)
                if pd.notna(labelProp):  # Ensure the label is valid
                    images.append(img)
                    labels.append(labelProp)
            except Exception as e:
                print(f"Error processing image {png_path}: {e}")

    return np.array(images), np.array(labels), png_paths, all_images

# Parameters and file paths
categories = ["Simple", "Extended", "Other", "Too_Noisy"]
burst_file_path = "pulse_shape_freq_with_analysis.csv"

# Process the dataset
data, labels, png_paths, all_images = process_csv(burst_file_path)
print(f"Total PNGs processed: {len(png_paths)}")
print(f"Images loaded: {data.shape[0]} | Labels loaded: {len(labels)}")

# Train a Random Forest classifier only if there is data
if len(data) > 0:
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        data, labels, test_size=0.20, stratify=labels, random_state=42
    )

    # Train a Random Forest classifier
    classifier = RandomForestClassifier(random_state=42)
    classifier.fit(X_train, y_train)

    y_pred = classifier.predict(X_test)
    train_pred = classifier.predict(X_train)
    print("Test Accuracy:", accuracy_score(y_test, y_pred))
    print("Train Accuracy:", accuracy_score(y_train, train_pred))




    # Predict on the full dataset
    predictions = classifier.predict(all_images)
else:
    predictions = []

# Prepare the predictions, filling in `Brother` for bursts without PNGs
full_predictions = []
count = 0

for idx in range(len(png_paths)):
    if png_paths[idx] is not None:  # If PNG exists, use the prediction
        full_predictions.append(predictions[count])
        count += 1
    else:  # Otherwise, set the prediction to "Brother"
        full_predictions.append("")

# Add the PNG paths and predictions to the original DataFrame
pulse_shape_df = pd.read_csv(burst_file_path)
pulse_shape_df["Burst_PNG"] = png_paths
pulse_shape_df["ML_Verify"] = full_predictions

# Save the updated DataFrame to a new CSV file
pulse_shape_df.to_csv("MachineLearning/pulse_shape_freq_with_ml.csv", index=False)
print("Updated pulse_shape_freq_with_ml.csv file saved successfully.")
