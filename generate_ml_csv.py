import pandas as pd
import numpy as np
import pickle

# Function to load the trained model and make predictions
def generate_ml_csv():
    # Load the processed image data
    processed_data = pd.read_csv("processed_images.csv")
    features = processed_data.drop(['Prop_Verify', '95%_Verify', '99%_Verify', 'png_path', 'Burst_Name'], axis=1).values
    png_paths = processed_data['png_path']

    # Load the trained model
    with open("random_forest_model.pkl", "rb") as f:
        classifier = pickle.load(f)

    # Predict using the classifier
    predictions = classifier.predict(features)

    # Load the original dataset
    burst_file_path = "pulse_shape_freq_with_analysis.csv"
    pulse_shape_df = pd.read_csv(burst_file_path)

    # Initialize columns for Burst_PNG and ML_Verify
    pulse_shape_df["Burst_PNG"] = None
    pulse_shape_df["ML_Verify"] = ""

    # Map predictions back to the original dataset based on matching burst names
    prediction_idx = 0
    for idx, row in pulse_shape_df.iterrows():
        burst_name = row["Burst_Name"]
        matching_pngs = png_paths[png_paths.str.contains(burst_name, na=False)]
        if not matching_pngs.empty:
            pulse_shape_df.at[idx, "Burst_PNG"] = matching_pngs.values[0]  # Assign matching PNG
            pulse_shape_df.at[idx, "ML_Verify"] = predictions[prediction_idx]  # Assign prediction
            prediction_idx += 1

    # Save the updated DataFrame to a new CSV file
    output_file = "pulse_shape_freq_with_ml.csv"
    pulse_shape_df.to_csv(output_file, index=False)
    print(f"Updated CSV file saved successfully as {output_file}")

if __name__ == "__main__":
    generate_ml_csv()
