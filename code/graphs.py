import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob

# --- plotting configuration ---
plt.rcParams.update({
    'font.size': 17,         
    'axes.labelsize': 17,   
    'axes.titlesize': 18,
    'xtick.labelsize': 15,   
    'ytick.labelsize': 15,   
    'legend.fontsize': 15,    
})
sns.set_style("whitegrid")

# --- read all .txt files in folder ---
files = glob.glob("*.txt")
df_list = []

for f in files:
    df = pd.read_csv(f, sep="|")
    df.columns = df.columns.str.strip()  # remove spaces in column names

    # remove rows with only dashes or invalid video names
    df = df[~df["Video"].str.contains("^-+$", regex=True)]
    
    # clean numeric values
    df["Time_s"] = df["Time_s"].astype(str).str.replace("s","", regex=False).astype(float)
    df["Energy_J"] = df["Energy_J"].astype(str).str.replace("J","", regex=False).astype(float)
    
    df_list.append(df)

# combine all dataframes
data = pd.concat(df_list, ignore_index=True)

# extract numeric resolution for sorting
data["Resolution_num"] = data["Resolution"].str.extract(r'(\d+)').astype(int)

# --- calculate normalized metrics ---
data["Time_per_s"] = data["Time_s"] / data["Time_s"]  # placeholder
data["Energy_per_s"] = data["Energy_J"] / data["Time_s"]
data["Energy_per_ProcTime"] = data["Energy_J"] / data["Time_s"]

# --- compute mean and std by video, codec, resolution ---
metrics = ["Time_s", "Energy_J", "Energy_per_ProcTime"]

summary = data.groupby(
    ["Video","Codec","Resolution","Resolution_num"]
)[metrics].agg(["mean","std"]).reset_index()

summary = summary.fillna(0)  # replace NaN std with 0

# --- function to plot metrics with std ---
def plot_metric_with_std(video_name, metric):
    clean_name = video_name.replace('.mp4','')
    plt.figure(figsize=(8,5))
    
    video_data = summary[summary["Video"]==video_name]
    codecs = video_data["Codec"].unique()
    
    # Mapeo por subcadena (funciona aunque los nombres tengan prefijos)
    mapeo = {
        '264': 'dodgerblue',   # h264
        '265': 'orange',      # h265
        'av1': 'red',         # av1
        'vp9': 'green'        # vp9
    }
    
    for codec in codecs:
        codec_data = video_data[video_data["Codec"]==codec].sort_values("Resolution_num")
        if codec_data.empty:
            continue

        x = codec_data["Resolution"]
        y = codec_data[(metric,"mean")]
        yerr = codec_data[(metric,"std")]

        # Buscar color por subcadena (case-insensitive)
        color = 'gray'  # color por defecto
        codec_lower = codec.lower()
        for key, col in mapeo.items():
            if key in codec_lower:
                color = col
                break

        # Dibujar línea y área con el color elegido
        plt.plot(x, y, label=codec, marker='o', color=color, linewidth=2)
        plt.fill_between(x, y - yerr, y + yerr, alpha=0.2, color=color)
    
    plt.xlabel("Resolution")
    labels = {
        "Time_s": "Processing time (s)",
        "Energy_J": "Energy (J)",
        "Energy_per_ProcTime": "Energy per processing time (J/s)"
    }
    plt.ylabel(labels[metric])
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{metric}_{clean_name}.png", dpi=300)
    plt.close()

# --- generate plots ---
videos = data["Video"].unique()
metrics_to_plot = ["Time_s","Energy_J","Energy_per_ProcTime"]

for video in videos:
    for metric in metrics_to_plot:
        plot_metric_with_std(video, metric)

print("All plots with mean and std generated successfully.")