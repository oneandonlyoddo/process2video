import argparse
import os
import subprocess
import sys
#path = "./process"

parser = argparse.ArgumentParser(description='Process Images to Video Sequence')

parser.add_argument('--in_path', help='The root path of the process folders')
parser.add_argument('--out_path', help='Where the video file will be saved')
parser.add_argument('--fps', type=float, help='Frames per second or speed of the video')
parser.add_argument('--filter_term', help='Only use frames with this term in their file path or name')

args = parser.parse_args()

process_path = args.in_path
video_out_path = args.out_path
fps = args.fps
filter_term = args.filter_term

def get_folders(path, depth=0, maxdepth=4):
    folders = os.listdir(path)
    folders = [path+"/"+folder for folder in folders if os.path.isdir(path+"/"+folder)]
    all_folders.extend(folders)
    if depth < maxdepth:
        for folder in folders:
            get_folders(folder , depth+1, 4)
    return all_folders

def is_image(image_path):
    allowed_extensions = [".gif", ".jpg", ".jpeg", ".png"]
    if os.path.exists(image_path):
        for extension in allowed_extensions:
            if image_path.lower().endswith(extension):
                return True
    return False
        
def get_images_from_folder(folder_path):
    files = os.listdir(folder_path)
    images = [folder_path+"/"+file for file in files if is_image(folder_path+"/"+file)]
    return images

def filter_by_term(file_paths, term):
    return [file_path for file_path in file_paths if term.lower() in file_path.lower()]

def write_file_list(files, out_path):
    with open(out_path,"w+") as f: 
        for file in files:
            f.write("file '" + file + "' \n") 
    print("file list written")
    return out_path
    
def ffmpeg_the_shit(file_list, out_path):
    cmd = "ffmpeg -y -f concat -r "+str(fps)+" -safe 0 -i "+file_list+" -vsync 0 -vcodec libx264 -vf \"scale=iw*min(1920/iw\,1080/ih):ih*min(1920/iw\,1080/ih), pad=1920:1080:(1920-iw*min(1920/iw\,1080/ih))/2:(1080-ih*min(1920/iw\,1080/ih))/2,format=yuv420p\" -r "+str(fps)+" -crf 20 -hide_banner "+ out_path
    print (cmd)
    return subprocess.call(cmd, shell=True)

all_folders = []
all_images = []

get_folders(process_path)

all_folders.sort()

for folder in all_folders:
    imgs = get_images_from_folder(folder)
    all_images.extend(imgs)
all_images.sort()

if filter_term != None:
    all_images = filter_by_term(all_images, filter_term)

out_path = write_file_list(all_images, "./files.txt")
exit_code = ffmpeg_the_shit(out_path, video_out_path)
print ("ffmpeg finished with exit code: " + str(exit_code))