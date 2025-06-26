import os
import pandas as pd
from skimage.io import imread
from skimage.transform import resize
import numpy as np


# Function to process images and labels
def process_csv(file_path, img_size=(32, 32), path_to_images="BurstPhotos"):
    images = []
    labels_prop = []
    labels_95 = []
    labels_99 = []
    png_paths = []
    burst_names = []  # To store Burst_Name
    count = 0

    file = pd.read_csv(file_path)
    for _, row in file.iterrows():
        print("Hello: " + row["Burst_PNG"])
        if row['Burst_PNG'] != "None":
            print(f"Processing Burst Name: {row['Burst_Name']}")
            png_path = path_to_images + "/" + row['Burst_PNG']
        else:
            png_path = False
        
        print(f"Working on item {count}")
        count += 1
        if png_path:  # Process only if a PNG exists
            print("PNG found.")
            try:
                img = imread(png_path)
                img = resize(img, img_size).flatten()  # Resize and flatten

                # Extract verification labels
                label_prop = row['Prop_Verify']
                label_95 = row['95%_Verify']
                label_99 = row['99%_Verify']

                # Append the data
                images.append(img)
                labels_prop.append(label_prop)
                labels_95.append(label_95)
                labels_99.append(label_99)
                png_paths.append(png_path.split("/")[-1])
                burst_names.append(row['Burst_Name'])
                print("Processed successfully.")
            except Exception as e:
                print(f"Error processing image {png_path}: {e}")

    # Save processed data to CSV
    processed_df = pd.DataFrame(images)
    processed_df['Prop_Verify'] = labels_prop
    processed_df['95%_Verify'] = labels_95
    processed_df['99%_Verify'] = labels_99
    processed_df['Burst_PNG'] = png_paths
    processed_df['Burst_Name'] = burst_names  # Include Burst_Name in the CSV
    processed_df.to_csv("ClassifiedBursts/Image_Labels.csv", index=False)
    print(f"Processed data saved to processed_images.csv")

if __name__ == "__main__":
    process_csv("ClassifiedBursts/Verified_Prop_Freq.csv")
