import subprocess
import time
import os

FFMPEG = "ffmpeg"

videos = ["glass_half.mp4", "sintel.mp4", "tearsofsteel.mp4", "wingit.mp4"]
resolutions = [(854, 480), (1280, 720), (1920, 1080)]

transcoding_settings = {
    "av1": {
        "container": "webm",
        "audio": "libopus",
        "video": "libsvtav1"
    },
    "h264": {
        "container": "mp4",
        "audio": "aac",
        "video": "libx264"
    },
    "h265": {
        "container": "mp4",
        "audio": "aac",
        "video": "libx265"
    },
    "vp9": {
        "container": "webm",
        "audio": "libopus",
        "video": "libvpx-vp9"
    }
}

input_dir = "input_videos"

def read_rapl_energy():
    try:
        with open("/sys/class/powercap/intel-rapl:0/energy_uj") as f:
            energy_uj = int(f.read().strip())
        return energy_uj / 1e6
    except:
        return 0


total_jobs = 5 * len(videos) * len(resolutions) * len(transcoding_settings)
job_counter = 0

print("\n========== STARTING FULL EXPERIMENT ==========\n")
print(f"Total transcodifications: {total_jobs}\n")

for run in range(1, 6):

    print(f"\n================ RUN {run}/5 ================\n")

    output_dir = f"output_run{run}"
    os.makedirs(output_dir, exist_ok=True)

    txt_file = os.path.join(output_dir, "transcoding_results.txt")

    with open(txt_file, mode='w') as f:

        f.write("Video | Codec | Resolution | Time_s | Energy_J\n")
        f.write("--------------------------------------------------\n")

        for video in videos:
            input_path = os.path.join(input_dir, video)

            for codec, settings in transcoding_settings.items():

                for width, height in resolutions:

                    job_counter += 1

                    print(f"\n[RUN {run}/5] [{job_counter}/{total_jobs}]")
                    print(f"→ Video: {video}")
                    print(f"→ Codec: {codec}")
                    print(f"→ Resolution: {width}x{height}")
                    print("Starting transcoding...")

                    output_file = os.path.join(
                        output_dir,
                        f"{os.path.splitext(video)[0]}_{codec}_{width}x{height}.{settings['container']}"
                    )

                    cmd = [
                        FFMPEG,
                        "-y",
                        "-i", input_path,
                        "-c:v", settings["video"],
                        "-vf", f"scale={width}:{height}",
                        "-c:a", settings["audio"],
                        output_file
                    ]

                    energy_before = read_rapl_energy()
                    time_before = time.time()

                    try:
                        subprocess.run(cmd, check=True)
                    except subprocess.CalledProcessError as e:
                        print(f"Error: {e}\n")
                        continue

                    energy_after = read_rapl_energy()
                    time_after = time.time()

                    energy_used = energy_after - energy_before
                    processing_time = time_after - time_before

                    result_line = (
                        f"{video} | {codec} | {width}x{height} | "
                        f"{processing_time:.2f}s | {energy_used:.2f}J"
                    )

                    print("Finished")
                    print(f"time: {processing_time:.2f} s")
                    print(f"energy: {energy_used:.2f} J")
                    print("-" * 50)

                    f.write(result_line + "\n")

    print(f"Run {run} completed. Results saved in {output_dir}\n")

print("========== ALL 5 RUNS COMPLETED ==========")
