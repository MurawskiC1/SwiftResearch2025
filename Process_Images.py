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
    burst_names = []
    count = 0

    file = pd.read_csv(file_path)

    for _, row in file.iterrows():
        burst_png = row["Burst_PNG"]
        
        if pd.notna(burst_png) and str(burst_png).strip() != "None":
            print(f"Processing Burst Name: {row['Burst_Name']}")
            png_path = os.path.join(path_to_images, str(burst_png))
        else:
            png_path = None

        print(f"Working on item {count}")
        count += 1

        if png_path:
            try:
                img = imread(png_path)
                img = resize(img, img_size).flatten()  # Resize and flatten to 1D array

                # Append image and labels
                images.append(img)
                labels_prop.append(row['Prop_Verify'])
                labels_95.append(row['95%_Verify'])
                labels_99.append(row['99%_Verify'])
                png_paths.append(str(burst_png))
                burst_names.append(row['Burst_Name'])

                print("Processed successfully.")
            except Exception as e:
                print(f"Error processing image {png_path}: {e}")

    # Convert image arrays to DataFrame
    image_df = pd.DataFrame(images)
    image_df['Prop_Verify'] = labels_prop
    image_df['95%_Verify'] = labels_95
    image_df['99%_Verify'] = labels_99
    image_df['Burst_PNG'] = png_paths
    image_df['Burst_Name'] = burst_names

    # Save to CSV
    image_df.to_csv("ClassifiedBursts/Image_Labels.csv", index=False)
    print("Processed data saved to ClassifiedBursts/Image_Labels.csv")

if __name__ == "__main__":
    process_csv("ClassifiedBursts/Verified_Prop_Freq.csv")
