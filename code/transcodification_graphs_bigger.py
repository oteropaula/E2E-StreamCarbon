import matplotlib.pyplot as plt

plt.rcParams.update({
    'font.size': 17,         
    'axes.labelsize': 17,   
    'axes.titlesize': 18,
    'xtick.labelsize': 15,   
    'ytick.labelsize': 15,   
    'legend.fontsize': 15,    
})


# --- 1. Full dataset ---
# Each entry contains video name, codec, target resolution, processing time (s), 
# energy consumption (J), and video duration (s)


data = [
    # Glass half
    {"Video": "glass_half.mp4", "Codec": "h264", "Resolution": "854x480", "ProcessingTime_s": 52.05, "Energy_J": 684.37, "Duration_s": 193.26},
    {"Video": "glass_half.mp4", "Codec": "h264", "Resolution": "1280x720", "ProcessingTime_s": 78.25, "Energy_J": 1080.79, "Duration_s": 193.26},
    {"Video": "glass_half.mp4", "Codec": "h264", "Resolution": "1920x1080", "ProcessingTime_s": 128.95, "Energy_J": 1792.72, "Duration_s": 193.26},
    {"Video": "glass_half.mp4", "Codec": "h265", "Resolution": "854x480", "ProcessingTime_s": 175.09, "Energy_J": 2241.06, "Duration_s": 193.26},
    {"Video": "glass_half.mp4", "Codec": "h265", "Resolution": "1280x720", "ProcessingTime_s": 293.08, "Energy_J": 3894.39, "Duration_s": 193.26},
    {"Video": "glass_half.mp4", "Codec": "h265", "Resolution": "1920x1080", "ProcessingTime_s": 544.81, "Energy_J": 7499.20, "Duration_s": 193.26},
    {"Video": "glass_half.mp4", "Codec": "vp9", "Resolution": "854x480", "ProcessingTime_s": 369.89, "Energy_J": 4283.54, "Duration_s": 193.26},
    {"Video": "glass_half.mp4", "Codec": "vp9", "Resolution": "1280x720", "ProcessingTime_s": 542.43, "Energy_J": 7168.49, "Duration_s": 193.26},
    {"Video": "glass_half.mp4", "Codec": "vp9", "Resolution": "1920x1080", "ProcessingTime_s": 945.68, "Energy_J": 12687.63, "Duration_s": 193.26},
    {"Video": "glass_half.mp4", "Codec": "av1", "Resolution": "854x480", "ProcessingTime_s": 75.01, "Energy_J": 966.58, "Duration_s": 193.26},
    {"Video": "glass_half.mp4", "Codec": "av1", "Resolution": "1280x720", "ProcessingTime_s": 109.77, "Energy_J": 1363.92, "Duration_s": 193.26},
    {"Video": "glass_half.mp4", "Codec": "av1", "Resolution": "1920x1080", "ProcessingTime_s": 184.07, "Energy_J": 2204.49, "Duration_s": 193.26},

    # Sintel
    {"Video": "sintel.mp4", "Codec": "h264", "Resolution": "854x480", "ProcessingTime_s": 18.56, "Energy_J": 262.68, "Duration_s": 52.21},
    {"Video": "sintel.mp4", "Codec": "h264", "Resolution": "1280x720", "ProcessingTime_s": 31.90, "Energy_J": 457.25, "Duration_s": 52.21},
    {"Video": "sintel.mp4", "Codec": "h264", "Resolution": "1920x1080", "ProcessingTime_s": 70.11, "Energy_J": 1014.28, "Duration_s": 52.21},
    {"Video": "sintel.mp4", "Codec": "h265", "Resolution": "854x480", "ProcessingTime_s": 88.09, "Energy_J": 1189.50, "Duration_s": 52.21},
    {"Video": "sintel.mp4", "Codec": "h265", "Resolution": "1280x720", "ProcessingTime_s": 151.05, "Energy_J": 2107.05, "Duration_s": 52.21},
    {"Video": "sintel.mp4", "Codec": "h265", "Resolution": "1920x1080", "ProcessingTime_s": 348.29, "Energy_J": 4875.25, "Duration_s": 52.21},
    {"Video": "sintel.mp4", "Codec": "vp9", "Resolution": "854x480", "ProcessingTime_s": 89.28, "Energy_J": 1047.02, "Duration_s": 52.21},
    {"Video": "sintel.mp4", "Codec": "vp9", "Resolution": "1280x720", "ProcessingTime_s": 116.45, "Energy_J": 1551.89, "Duration_s": 52.21},
    {"Video": "sintel.mp4", "Codec": "vp9", "Resolution": "1920x1080", "ProcessingTime_s": 189.11, "Energy_J": 2527.92, "Duration_s": 52.21},
    {"Video": "sintel.mp4", "Codec": "av1", "Resolution": "854x480", "ProcessingTime_s": 15.83, "Energy_J": 219.08, "Duration_s": 52.21},
    {"Video": "sintel.mp4", "Codec": "av1", "Resolution": "1280x720", "ProcessingTime_s": 23.85, "Energy_J": 320.98, "Duration_s": 52.21},
    {"Video": "sintel.mp4", "Codec": "av1", "Resolution": "1920x1080", "ProcessingTime_s": 51.65, "Energy_J": 706.03, "Duration_s": 52.21},

    # Tears of Steel
    {"Video": "tearsofsteel.mp4", "Codec": "h264", "Resolution": "854x480", "ProcessingTime_s": 61.82, "Energy_J": 865.89, "Duration_s": 116.56},
    {"Video": "tearsofsteel.mp4", "Codec": "h264", "Resolution": "1280x720", "ProcessingTime_s": 101.86, "Energy_J": 1435.29, "Duration_s": 116.56},
    {"Video": "tearsofsteel.mp4", "Codec": "h264", "Resolution": "1920x1080", "ProcessingTime_s": 244.68, "Energy_J": 3450.86, "Duration_s": 116.56},
    {"Video": "tearsofsteel.mp4", "Codec": "h265", "Resolution": "854x480", "ProcessingTime_s": 269.94, "Energy_J": 3690.89, "Duration_s": 116.56},
    {"Video": "tearsofsteel.mp4", "Codec": "h265", "Resolution": "1280x720", "ProcessingTime_s": 484.96, "Energy_J": 6757.21, "Duration_s": 116.56},
    {"Video": "tearsofsteel.mp4", "Codec": "h265", "Resolution": "1920x1080", "ProcessingTime_s": 1154.30, "Energy_J": 16155.51, "Duration_s": 116.56},
    {"Video": "tearsofsteel.mp4", "Codec": "vp9", "Resolution": "854x480", "ProcessingTime_s": 260.11, "Energy_J": 3074.76, "Duration_s": 116.56},
    {"Video": "tearsofsteel.mp4", "Codec": "vp9", "Resolution": "1280x720", "ProcessingTime_s": 333.85, "Energy_J": 4556.00, "Duration_s": 116.56},
    {"Video": "tearsofsteel.mp4", "Codec": "vp9", "Resolution": "1920x1080", "ProcessingTime_s": 606.22, "Energy_J": 8294.54, "Duration_s": 116.56},
    {"Video": "tearsofsteel.mp4", "Codec": "av1", "Resolution": "854x480", "ProcessingTime_s": 41.43, "Energy_J": 589.87, "Duration_s": 116.56},
    {"Video": "tearsofsteel.mp4", "Codec": "av1", "Resolution": "1280x720", "ProcessingTime_s": 56.38, "Energy_J": 781.34, "Duration_s": 116.56},
    {"Video": "tearsofsteel.mp4", "Codec": "av1", "Resolution": "1920x1080", "ProcessingTime_s": 101.24, "Energy_J": 1415.79, "Duration_s": 116.56},

    # Wingit
    {"Video": "wingit.mp4", "Codec": "h264", "Resolution": "854x480", "ProcessingTime_s": 87.54, "Energy_J": 1249.15, "Duration_s": 237.98},
    {"Video": "wingit.mp4", "Codec": "h264", "Resolution": "1280x720", "ProcessingTime_s": 145.21, "Energy_J": 2088.38, "Duration_s": 237.98},
    {"Video": "wingit.mp4", "Codec": "h264", "Resolution": "1920x1080", "ProcessingTime_s": 230.62, "Energy_J": 3341.64, "Duration_s": 237.98},
    {"Video": "wingit.mp4", "Codec": "h265", "Resolution": "854x480", "ProcessingTime_s": 319.63, "Energy_J": 4401.23, "Duration_s": 237.98},
    {"Video": "wingit.mp4", "Codec": "h265", "Resolution": "1280x720", "ProcessingTime_s": 605.29, "Energy_J": 8499.20, "Duration_s": 237.98},
    {"Video": "wingit.mp4", "Codec": "h265", "Resolution": "1920x1080", "ProcessingTime_s": 1071.35, "Energy_J": 15106.83, "Duration_s": 237.98},
    {"Video": "wingit.mp4", "Codec": "vp9", "Resolution": "854x480", "ProcessingTime_s": 535.56, "Energy_J": 6258.94, "Duration_s": 237.98},
    {"Video": "wingit.mp4", "Codec": "vp9", "Resolution": "1280x720", "ProcessingTime_s": 723.99, "Energy_J": 9672.47, "Duration_s": 237.98},
    {"Video": "wingit.mp4", "Codec": "vp9", "Resolution": "1920x1080", "ProcessingTime_s": 1232.35, "Energy_J": 16699.53, "Duration_s": 237.98},
    {"Video": "wingit.mp4", "Codec": "av1", "Resolution": "854x480", "ProcessingTime_s": 94.90, "Energy_J": 1340.56, "Duration_s": 237.98},
    {"Video": "wingit.mp4", "Codec": "av1", "Resolution": "1280x720", "ProcessingTime_s": 139.47, "Energy_J": 1942.87, "Duration_s": 237.98},
    {"Video": "wingit.mp4", "Codec": "av1", "Resolution": "1920x1080", "ProcessingTime_s": 221.40, "Energy_J": 3062.46, "Duration_s": 237.98},
]

# --- 2. Compute normalized metrics ---
# Calculate processing time per second of video, energy per second, and energy per processing second
for entry in data:
    entry["Time_per_s"] = entry["ProcessingTime_s"] / entry["Duration_s"]
    entry["Energy_per_s"] = entry["Energy_J"] / entry["Duration_s"]
    entry["Energy_per_ProcTime"] = entry["Energy_J"] / entry["ProcessingTime_s"]

# --- 3. Plotting functions by video ---
def plot_processing_time_by_video(video_name):
    clean_name = video_name.replace('.mp4','')
    codecs = ["h264", "h265", "vp9", "av1"]
    resolutions = ["854x480", "1280x720", "1920x1080"]

    # Create figure and plot processing time for each codec
    plt.figure(figsize=(8,5))
    for codec in codecs:
        times = [entry["ProcessingTime_s"] for entry in data if entry["Video"]==video_name and entry["Codec"]==codec]
        plt.plot(resolutions, times, marker='o', label=codec)
    plt.xlabel('Resolution')
    plt.ylabel('Processing Time (s)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"processing_time_{clean_name}.png", dpi=300)
    plt.close()

def plot_energy_by_video(video_name):
    clean_name = video_name.replace('.mp4','')
    codecs = ["h264", "h265", "vp9", "av1"]
    resolutions = ["854x480", "1280x720", "1920x1080"]

    # Plot energy consumption for each codec
    plt.figure(figsize=(8,5))
    for codec in codecs:
        energies = [entry["Energy_J"] for entry in data if entry["Video"]==video_name and entry["Codec"]==codec]
        plt.plot(resolutions, energies, marker='o', label=codec)
    plt.xlabel('Resolution')
    plt.ylabel('Energy (J)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"energy_{clean_name}.png", dpi=300)
    plt.close()

def plot_energy_per_proc_time_by_video(video_name):
    clean_name = video_name.replace('.mp4','')
    codecs = ["h264", "h265", "vp9", "av1"]
    resolutions = ["854x480", "1280x720", "1920x1080"]

    # Plot energy per processing second (J/s processed)
    plt.figure(figsize=(8,5))
    for codec in codecs:
        values = [entry["Energy_per_ProcTime"] for entry in data if entry["Video"]==video_name and entry["Codec"]==codec]
        plt.plot(resolutions, values, marker='o', label=codec)
    plt.xlabel('Resolution')
    plt.ylabel('Energy / Processing Time (J/s processed)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"energy_per_proc_time_{clean_name}.png", dpi=300)
    plt.close()

# --- 4. Generate plots for all videos ---
videos = ["glass_half.mp4", "sintel.mp4", "tearsofsteel.mp4", "wingit.mp4"]
for video in videos:
    plot_processing_time_by_video(video)
    plot_energy_by_video(video)
    plot_energy_per_proc_time_by_video(video)

print("All plots generated and saved successfully.")