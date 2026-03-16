import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# list of videos to analyze
video_paths = [
    "sintel.mp4",
    "wingit.mp4",
    "tearsofsteel.mp4",
    "glass_half.mp4"
]

# colors to use for each video
colors = ['darkred', 'lightcoral', 'lightgrey', 'dimgray']

# folder to save the plots
output_folder = "./"
os.makedirs(output_folder, exist_ok=True)

# dictionary to store the average spatial complexity for each video
complexity_scores = {}

for idx, video_path in enumerate(video_paths):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"error: could not open {video_path}")
        continue

    spatial_scores = []
    frame_indices = []

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # calculate spatial complexity as the variance of the frame
        spatial_score = np.var(gray)
        spatial_scores.append(spatial_score)
        frame_indices.append(frame_count)

        frame_count += 1

    # release the video capture
    cap.release()

    # calculate the average spatial complexity
    avg_spatial = np.mean(spatial_scores)
    complexity_scores[os.path.basename(video_path)] = avg_spatial

    # create a new figure for the video
    plt.figure(figsize=(12, 5))
    plt.plot(frame_indices, spatial_scores, color=colors[idx], linestyle='-')

    # label the axes and set title
    plt.xlabel('frame')
    plt.ylabel('spatial complexity (variance of pixel intensities)')
    plt.title(f'spatial complexity - {os.path.basename(video_path)}')

    # add a legend showing the average complexity
    plt.legend([f"average spatial complexity: {avg_spatial:.2f}"], loc='upper right')

    # make layout tight
    plt.tight_layout()

    # save the figure
    output_image = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(video_path))[0]}_spatial_complexity.png")
    plt.savefig(output_image)
    plt.close()
    print(f"graph saved as: {output_image} | average spatial complexity: {avg_spatial:.2f}")

# sort videos from highest to lowest average spatial complexity
sorted_videos = sorted(complexity_scores.items(), key=lambda x: x[1], reverse=True)
print("\nvideos sorted by average spatial complexity (high → low):")
for video, score in sorted_videos:
    print(f"{video}: {score:.2f}")
