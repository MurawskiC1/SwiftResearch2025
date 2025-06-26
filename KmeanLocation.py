import numpy as np
import pandas as pd
import ast
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# Load data from PulseLocation.csv
input_file = "CSVExports/Pulse_Location.csv"
output_file = "ClassifiedBursts/Pulse_Location_Narrowed.csv"

# Read CSV file
df = pd.read_csv(input_file)

# Max number of clusters to consider
max_clusters = 5  # Adjust based on possible clusters

# Store results for best boxes and cluster info
all_results = []

# Loop through each burst row
for i, row in df.iterrows():
    try:
        # Parse the lists from string to numeric
        x_coords = np.array(ast.literal_eval(row["X_Locations"]))
        y_coords = np.array(ast.literal_eval(row["Y_Locations"]))
        widths = np.array(ast.literal_eval(row["Widths"]))
        heights = np.array(ast.literal_eval(row["Heights"]))

        # Convert to bounding box format: [x_min, y_min, x_max, y_max]
        boxes = np.vstack([x_coords, y_coords, x_coords + widths, y_coords + heights]).T
    #,
        # Automatically determine the best number of clusters using silhouette score
        best_k = 1
        best_score = -1

        for k in range(2, min(len(boxes), max_clusters) + 1):
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = kmeans.fit_predict(boxes)
            score = silhouette_score(boxes, labels)

            if score > best_score:
                best_score = score
                best_k = k

        # Apply K-means with optimal clusters
        kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=10)
        kmeans.fit(boxes)

        # Get cluster centers (centroids)
        centroids = kmeans.cluster_centers_

        # Count number of clusters with significant points
        labels, counts = np.unique(kmeans.labels_, return_counts=True)
        valid_clusters = labels[counts > 3]  # Keep clusters with 3+ boxes

        has_multiple_clusters = len(valid_clusters) > 1

        # Store all valid boxes with multiple clusters if applicable
        for cluster in valid_clusters:
            best_box = centroids[cluster]
            all_results.append([
                row["Burst Name"],
                best_box[0], best_box[1], best_box[2], best_box[3],
                best_k,
                has_multiple_clusters
            ])

        print(f"✅ Processed: {row['Burst Name']}  with {len(valid_clusters)} clusters")

    except Exception as e:
        print(f"❌ Error processing row {i}: {e}")
        all_results.append([
            row["Burst Name"], np.nan, np.nan, np.nan, np.nan, np.nan, False
        ])

# Create DataFrame with results
df_result = pd.DataFrame(
    all_results,
    columns=[
        "Burst Name", "x_min", "y_min", "x_max", "y_max",
        "num_clusters", "has_multiple_clusters"
    ]
)

# Save results to a new CSV file
df_result.to_csv(output_file, index=False)
print(f"🎉 Results with multiple clusters saved to {output_file}")

