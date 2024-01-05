import os
import cv2
import numpy as np
from PIL import Image
from moviepy.editor import *
# from annotator.dwpose import DWposeDetector
from controlnet_aux import DWposeDetector
import matplotlib.pyplot as plt
import torch

det_config  = "yolox_l_8xb8-300e_coco.py"
det_ckpt = "https://download.openmmlab.com/mmdetection/v2.0/yolox/yolox_l_8x8_300e_coco/yolox_l_8x8_300e_coco_20211126_140236-d3bd2b23.pth"
pose_config = "dwpose-l_384x288.py"
pose_ckpt = "dw-ll_ucoco_384.pth"

device = torch.device('cuda:3')
pose = DWposeDetector(det_config=det_config, det_ckpt=det_ckpt, pose_config=pose_config, pose_ckpt=pose_ckpt, device=device)

def get_frames(video_in):
    frames = []
    # 调整视频大小
    clip = VideoFileClip(video_in)
    clip_resized = clip.resize(height=512, width=512)
    clip_resized.write_videofile("output_imgs/video_resized.mp4")

    # 打开调整大小后的视频
    cap = cv2.VideoCapture("output_imgs/video_resized.mp4")
    fps = cap.get(cv2.CAP_PROP_FPS)
    print("video fps: " + str(fps))

    i = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        cv2.imwrite('output_imgs/frame_'+str(i)+'.jpg', frame)
        frames.append('output_imgs/frame_'+str(i)+'.jpg')
        i += 1

    cap.release()
    cv2.destroyAllWindows()
    print("broke the video into frames")

    return frames, fps

def get_openpose_filter(frame_path):
    oriImg = cv2.imread(frame_path)  # B,G,R order
    out = pose(oriImg)
    out = np.array(out)
    image = Image.fromarray(out)
    frame_name = os.path.basename(frame_path)
    image.save("output_imgs/openpose_" + frame_name)
    return "output_imgs/openpose_" + frame_name

def create_video(frames, fps, type):
    print("building video result")
    clip = ImageSequenceClip(frames, fps=fps)
    output_path = os.path.join(type + ".mp4")
    clip.write_videofile(output_path, fps=fps)
    return output_path

def infer():

    # # 1. 获取另一个文件夹中的视频列表
    # exclude_folder = "/home/liuxinyi/jinyuxin/train_dwpose/"  # 不包含的视频文件夹路径
    # exclude_videos = set(os.listdir(exclude_folder))

    # 1. 遍历文件夹下的所有视频
    video_folder = "/home/liuxinyi/jinyuxin/DWPose/img/"  # 视频所在文件夹路径
    output_folder = "/home/liuxinyi/jinyuxin/DWPose/img_dep/"  # 输出视频的文件夹路径
    videos = os.listdir(video_folder)

    for video in videos:
        # if video in exclude_videos:
        #     continue
        video_in = os.path.join(video_folder, video)
        print("Processing video:", video)

        # 2. 将视频分解为帧，并获取帧率
        break_vid = get_frames(video_in)
        frames_list = break_vid[0]
        fps = break_vid[1]
        n_frame = len(frames_list)

        if n_frame >= len(frames_list):
            print("video is shorter than the cut value")
            n_frame = len(frames_list)

        # 3. 准备帧的结果数组
        result_frames = []
        print("set stop frames to:", n_frame)

        for i in frames_list[0:int(n_frame)]:
            openpose_frame = get_openpose_filter(i)
            result_frames.append(openpose_frame)
            print("frame", i, "/", n_frame, ": done;")

        # 4. 创建姿势（pose）视频并保存
        final_vid = create_video(result_frames, fps, output_folder + os.path.splitext(video)[0])
        print("Pose video created:", final_vid)
        print()

infer()