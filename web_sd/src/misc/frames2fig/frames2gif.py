import os
import imageio
import re

def find_images(folder_path, prefix):
    pattern = re.compile(rf"{prefix}_(\d+)_\.png")
    
    file_path_list = sorted(
        [f for f in os.listdir(folder_path) if pattern.match(f)],
        key=lambda x: int(pattern.match(x).group(1))
    )

    file_path_list = [os.path.join(folder_path, f) for f in file_path_list]
    return file_path_list

def load_images(file_path_list):
    images = []
    for file_path in file_path_list:
        images.append(imageio.imread(file_path))

    return images

def create_gif(images, output_filename):
    imageio.mimsave(output_filename, images, duration=0.1)

def main():
    get_data_from = "../output/"
    output_path = "fs/sample.gif"
    # as system path
    full_os_path = os.path.abspath(get_data_from)
    print(full_os_path)
    frames_paths = find_images(full_os_path, "eeg")
    # frames_paths = frames_paths[:100]
    images = load_images(frames_paths)
    print(f"len images: {len(images)}")
    create_gif(images, output_path)

main()

# TODO:
# - meaby stright to mp4 (ffmpeg)
# - add argparse for in folder and out file