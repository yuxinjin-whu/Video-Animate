from moviepy.editor import ImageSequenceClip
import os
import glob

def create_video_from_images(image_folder, output_folder, video_name, fps=25, img_ext=".png"):
    images = sorted(glob.glob(os.path.join(image_folder, '*' + img_ext)), key=os.path.getmtime)
    if images:
        clip = ImageSequenceClip(images, fps=fps)
        clip.write_videofile(os.path.join(output_folder, video_name), codec='libx264')

def process_all_folders(root_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for subdir in os.listdir(root_folder):
        dir_path = os.path.join(root_folder, subdir)
        if os.path.isdir(dir_path):
            images_folder = os.path.join(dir_path, "images")
            if os.path.exists(images_folder):
                video_name = f"{subdir}.mp4"
                create_video_from_images(images_folder, output_folder, video_name)
                print(f"Video saved as {os.path.join(output_folder, video_name)}")
            else:
                print(f"No 'images' folder found in {dir_path}")

root_directory = "TikTok_dataset"  # Replace with your root directory path
output_directory = "TikTok_processed" # Replace with your output directory path
process_all_folders(root_directory, output_directory)