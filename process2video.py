#import argparse
import os
import subprocess
import sys
#path = "./process"
process_path = sys.argv[1]
video_out_path = sys.argv[2]
fps = sys.argv[3]

all_folders = []
all_images = []

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

def write_file_list(files, out_path):
    with open(out_path,"w+") as f: 
        for file in files:
            f.write("file '" + file + "' \n") 
    print("file list written")
    return out_path
    
def ffmpeg_the_shit(file_list, out_path):
    #cmd = ["ffmpeg", "-f", "concat", "-r", "1/2", "-i", file_list, "-crf", "20", "-vf", "fps=8", "format=yuv420p", out_path]
    #cmd = "ffmpeg -y -f concat -r 1/2 -safe 0 -i "+file_list+" -crf 20 -vf fps=8 "+ out_path
    cmd = "ffmpeg -y -f concat -r "+fps+" -safe 0 -i "+file_list+" -vsync 0 -vf 'scale=iw*min(1920/iw\,1080/ih):ih*min(1920/iw\,1080/ih), pad=1920:1080:(1920-iw*min(1920/iw\,1080/ih))/2:(1080-ih*min(1920/iw\,1080/ih))/2,format=yuv420p' -r "+fps+" -crf 20 "+ out_path
    #params = ["-f", "concat", "-r", "1/2", "-i", list.txt -vf "scale=iw*min(1920/iw\,1080/ih):ih*min(1920/iw\,1080/ih), pad=1920:1080:(1920-iw*min(1920/iw\,1080/ih))/2:(1080-ih*min(1920/iw\,1080/ih))/2,fps=8,format=yuv420p" -crf 20 video.mp4
    
    print (cmd)
    subprocess.call(cmd, shell=True)

get_folders(process_path)

all_folders.sort()

for folder in all_folders:
    imgs = get_images_from_folder(folder)
    all_images.extend(imgs)
all_images.sort()

out_path = write_file_list(all_images, "./files.txt")
exit_code = ffmpeg_the_shit(out_path, video_out_path)
print (exit_code)