import pandas as pd
import numpy as np
import pickle

def generate_ml_csv():
    # Load the processed image data
    processed_data = pd.read_csv("ClassifiedBursts/Image_Labels.csv")

    # Extract only the image features (drop label columns and metadata)
    feature_columns = processed_data.columns.difference(['Prop_Verify', '95%_Verify', '99%_Verify', 'Burst_PNG', 'Burst_Name'])
    features = processed_data[feature_columns].values
    burst_names = processed_data["Burst_Name"]
    burst_pngs = processed_data["Burst_PNG"]

    # Load the trained classifier
    with open("MachineLearning/rf_model.pkl", "rb") as f:
        classifier = pickle.load(f)

    # Make predictions
    predictions = classifier.predict(features)

    # Load the target CSV to update
    pulse_shape_df = pd.read_csv("ClassifiedBursts/Verified_Prop_Freq.csv")

    # Add ML columns if they don't already exist
    if "ML_Verify" not in pulse_shape_df.columns:
        pulse_shape_df["ML_Verify"] = ""
    if "Burst_PNG" not in pulse_shape_df.columns:
        pulse_shape_df["Burst_PNG"] = ""

    # Map predictions to pulse_shape_df by matching Burst_Name
    for i in range(len(burst_names)):
        name = burst_names[i]
        match = pulse_shape_df["Burst_Name"] == name
        if match.any():
            idx = pulse_shape_df[match].index[0]
            pulse_shape_df.at[idx, "ML_Verify"] = predictions[i]
            pulse_shape_df.at[idx, "Burst_PNG"] = burst_pngs[i]

    # Save updated CSV
    output_path = "MachineLearning/pulse_shape_freq_with_ml.csv"
    pulse_shape_df.to_csv(output_path, index=False)
    print(f"✅ ML predictions added and saved to: {output_path}")

if __name__ == "__main__":
    generate_ml_csv()
