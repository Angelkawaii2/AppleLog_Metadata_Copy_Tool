import argparse
import os
import subprocess
import threading
import time
from concurrent.futures import ProcessPoolExecutor, as_completed, ThreadPoolExecutor

# 创建一个锁对象用于线程安全的更新进度计数
progress_lock = threading.Lock()
total_tasks = 0
completed_tasks = 0


def process_video(args):
    global completed_tasks
    original_video_path, rendered_video_path, output_video_path = args
    start_time = time.time()
    # 执行 ffmpeg 命令
    ffmpeg_cmd = [
        "ffmpeg",
        "-i", original_video_path,
        "-i", rendered_video_path,
        "-map", "1",
        "-c", "copy",
        "-movflags", "use_metadata_tags",
        "-map_metadata", "0",
        "-loglevel", "warning",
        output_video_path
    ]
    subprocess.run(ffmpeg_cmd, stdout=subprocess.DEVNULL)

    # 执行 exiftool 命令来更新元数据
    exiftool_cmd = [
        "exiftool",
        "-m",
        "-P",
        "-overwrite_original",
        "-All=",
        "-tagsFromFile", "@",
        "-All:All",
        "-Unsafe",
        "-ICC_Profile",
        output_video_path
    ]
    subprocess.run(exiftool_cmd, stdout=subprocess.DEVNULL)
    end_time = time.time()
    elapsed_time = end_time - start_time
    # 更新进度和打印信息
    with progress_lock:
        completed_tasks += 1
        print(
            f"Processed {os.path.basename(output_video_path)} | Time: {elapsed_time:.2f} sec | Progress: {completed_tasks}/{total_tasks} Remaining: {total_tasks - completed_tasks}")


def main():
    global total_tasks
    parser = argparse.ArgumentParser(description="Concurrently process videos using ffmpeg and exiftool.")
    parser.add_argument("-o", "--path_orig", help="Path to the original ProRes video files.")
    parser.add_argument("-r", "--path_rendered", help="Path to the rendered video files.")
    parser.add_argument("-p", "--path_output", help="Output path for the final video files.")
    args = parser.parse_args()

    if not args.path_orig:
        args.path_orig = input("Enter the path to the original ProRes video files: ")
    if not args.path_rendered:
        args.path_rendered = input("Enter the path to the rendered video files: ")
    if not args.path_output:
        args.path_output = input("Enter the output path for the final video files: ")

    if not os.path.exists(args.path_output):
        os.makedirs(args.path_output)

    tasks = []
    for original_video in os.listdir(args.path_orig):
        if original_video.endswith(".MOV"):
            original_video_path = os.path.join(args.path_orig, original_video)
            rendered_videos = [f for f in os.listdir(args.path_rendered) if original_video in f]
            if not rendered_videos:
                print(f"[Note] Rendered file for {original_video} not found.")
                continue

            for rendered_video in rendered_videos:
                rendered_video_path = os.path.join(args.path_rendered, rendered_video)
                output_video_path = os.path.join(args.path_output, original_video)
                tasks.append((original_video_path, rendered_video_path, output_video_path))

    total_tasks = len(tasks)

    # 使用 ThreadPoolExecutor 并发处理视频
    # 在执行ExifTool处理远程服务器上视频的时候不知道为什么奇慢无比，也没有看到CPU和网络大量占用，所以用多线程能快不少（吃满带宽和U）
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_video, task) for task in tasks]
        for future in as_completed(futures):
            future.result()

    print("===========All videos processed.============")


if __name__ == "__main__":
    main()
