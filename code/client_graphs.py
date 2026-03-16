import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams.update({
    'font.size': 17,
    'axes.labelsize': 17,
    'axes.titlesize': 18,
    'xtick.labelsize': 15,
    'ytick.labelsize': 15,
    'legend.fontsize': 15,
})

sns.set_style("whitegrid")

data = {
    "glass_half.mp4": {
        "h264": [993.628377, 1085.407926, 1199.262922],
        "h265": [1013.963773, 1202.519382, 1529.149163],
        "vp9":  [970.983049, 991.263637, 996.042982],
        "av1":  [1058.477820, 1090.892227, 1079.352340],
    },
    "sintel.mp4": {
        "h264": [302.644917, 340.022262, 490.463893],
        "h265": [333.098635, 395.158351, 638.661817],
        "vp9":  [289.515677, 292.758589, 290.960987],
        "av1":  [327.012713, 288.910515, 294.736856],
    },
    "tearsofsteel.mp4": {
        "h264": [728.837367, 902.434702, 1658.160733],
        "h265": [825.503563, 1111.650902, 1960.755845],
        "vp9":  [605.329200, 623.029106, 613.426897],
        "av1":  [586.254359, 595.760010, 608.524931],
    },
    "wingit.mp4": {
        "h264": [1367.956825, 1499.775335, 1724.134807],
        "h265": [1416.350195, 1787.950135, 2368.350077],
        "vp9":  [1244.105335, 1267.699941, 1281.882461],
        "av1":  [1224.450661, 1267.688405, 1289.063778],
    }
}

# --- X axis: numeric positions + labels ---
resolutions_labels = ["854x480", "1280x720", "1920x1080"]
resolutions_num = [480, 720, 1080]  # usamos altura como valor numérico para spacing proporcional

colors = {
    "h264": "dodgerblue",
    "h265": "orange",
    "av1":  "red",
    "vp9":  "green",
}

for video, codecs in data.items():
    clean_name = video.replace(".mp4", "")
    fig, ax = plt.subplots(figsize=(8,5))

    for codec in ["h264", "h265", "vp9", "av1"]:
        ax.plot(
            resolutions_num,
            codecs[codec],
            marker='o',
            label=codec,
            color=colors[codec],
            linewidth=2
        )

    # --- gray border / spines ---
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color('#cccccc')
        spine.set_linewidth(1)

    # --- grid ---
    ax.grid(True, linestyle='-', alpha=0.3)

    # --- X axis: numeric positions + labels ---
    ax.set_xticks(resolutions_num)
    ax.set_xticklabels(resolutions_labels)

    # opcional: fijar límites para que quede consistente entre videos
    ax.set_xlim(450, 1110)

    ax.set_xlabel("Resolution")
    ax.set_ylabel("Energy (J)")
    ax.legend()

    plt.tight_layout()
    plt.savefig(f"client_energy_{clean_name}.png", dpi=300)
    plt.close()

print("Client-side energy plots generated successfully.")