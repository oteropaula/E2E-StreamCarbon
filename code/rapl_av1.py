import subprocess
import time
import os

FFMPEG = "/home/lrk/bin/ffmpeg"

videos = ["glass_half.mp4", "sintel.mp4", "tearsofsteel.mp4", "wingit.mp4"]

resolutions = [(854, 480), (1280, 720), (1920, 1080)]

transcoding_settings = {
    "av1": {"container": "webm", "audio": "libopus", "video": "libsvtav1"}
}

input_dir = "input_videos"
output_dir = "output_videos"
os.makedirs(output_dir, exist_ok=True)

def read_rapl_energy():
    """Lee energía desde RAPL en julios."""
    try:
        with open("/sys/class/powercap/intel-rapl:0/energy_uj") as f:
            energy_uj = int(f.read().strip())
        return energy_uj / 1e6
    except Exception as e:
        print(f"Error reading energy: {e}")
        return 0

txt_file = os.path.join(output_dir, "transcoding_results_av1.txt")

with open(txt_file, mode='w') as f:
    f.write("Video | Codec | Resolution | ProcessingTime_s | Energy_J\n")
    f.write("-----------------------------------------------------------\n")

    for video in videos:
        input_path = os.path.join(input_dir, video)
        for codec, settings in transcoding_settings.items():
            for width, height in resolutions:
                output_file = os.path.join(output_dir, f"{os.path.splitext(video)[0]}_{codec}_{width}x{height}.{settings['container']}")

                cmd = [
                    FFMPEG, "-i", input_path,
                    "-c:v", settings["video"],
                    "-crf", "0", "-b:v", "512k",
                    "-vf", f"scale={width}:{height}",
                    "-c:a", settings["audio"],
                    output_file
                ]

                print(f"Running: {video} | {codec} | {width}x{height}")

                energy_before = read_rapl_energy()
                time_before = time.time()

                try:
                    subprocess.run(cmd, check=True)
                except subprocess.CalledProcessError as e:
                    print(f"Error transcoding {video} at {width}x{height}: {e}")
                    continue

                energy_after = read_rapl_energy()
                time_after = time.time()

                energy_consumed = energy_after - energy_before
                processing_time = time_after - time_before

                print(f"Energy consumed: {energy_consumed:.2f} J | Processing time: {processing_time:.2f} s")

                f.write(f"{video} | {codec} | {width}x{height} | {processing_time:.2f} | {energy_consumed:.2f}\n")

print(f"All transcoding done. Results saved in {txt_file}")

