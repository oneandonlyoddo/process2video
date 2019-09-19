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
parser.add_argument('--blacklist_term', help='Only use frames without this term in their file path or name')

args = parser.parse_args()

process_path = args.in_path
video_out_path = args.out_path
fps = args.fps
filter_term = args.filter_term
blacklist_terms = args.blacklist_term

def get_folders(path, depth=0, maxdepth=4):
    folders = os.listdir(path)
    folders = [os.path.join(path,folder) for folder in folders if os.path.isdir(os.path.join(path,folder))]
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
    images = [os.path.join(folder_path,file) for file in files if is_image(os.path.join(folder_path, file))]
    return images

def filter_by_term(file_paths, term):
    return [file_path for file_path in file_paths if term.lower() in file_path.lower()]

def blacklist_by_terms(file_paths, terms):
    for term in terms:
        file_paths = [file_path for file_path in file_paths if term.lower() not in file_path.lower()]
    return file_paths

def write_file_list(files, out_path):
    with open(out_path,"w+") as f: 
        for file in files:
            file = file.replace("\\", "/" )
            f.write("file '" + file + "' \n") 
    print_info(" file list written")
    return out_path

def filter_out_hidden_files(file_paths):
    return [file_path for file_path in file_paths if not os.path.basename(file_path).startswith('.')]

def ffmpeg_the_shit(file_list, out_path):
    cmd = "ffmpeg -hide_banner -r "+str(fps)+" -y -f concat -safe 0 -i "+file_list+" -vsync 0  -vcodec libx264 -vf \"scale=iw*min(1920/iw\,1080/ih):ih*min(1920/iw\,1080/ih), pad=1920:1080:(1920-iw*min(1920/iw\,1080/ih))/2:(1080-ih*min(1920/iw\,1080/ih))/2,fps="+str(fps)+",format=yuv420p\" -crf 20 -hide_banner "+ out_path
    #print (cmd)
    return subprocess.call(cmd, shell=True)

def print_line():
    print('\033[95m'+"----------------------------------------------------------------------------------" + '\033[0m')

def print_info(info_text):
    #prints in green
    print('\033[92m' + info_text + '\033[0m')

def print_warning(warning_text):
    #prints in red
    print('\033[91m' + warning_text + '\033[0m')

os.system('color')

print_line()

all_folders = []
all_images = []

get_folders(process_path)

all_folders.sort()

for folder in all_folders:
    imgs = get_images_from_folder(folder)
    all_images.extend(imgs)
all_images.sort()

all_images = filter_out_hidden_files(all_images)

if filter_term != None:
    all_images = filter_by_term(all_images, filter_term)

if blacklist_terms != None:
    terms = blacklist_terms.split(",")
    terms = [term.strip() for term in terms]
    all_images = blacklist_by_terms(all_images, terms)

print_info(" found %d images that match the specified criteria" % (len(all_images)) )

out_path = write_file_list(all_images, "./files.txt")

print_info(" starting ffmpeg process" )

print_line()

exit_code = ffmpeg_the_shit("files.txt", video_out_path)

print_line()

if exit_code == 0:
    print_info(" ffmpeg succesfully finished. Find your video file here: %s" % (video_out_path))
else:
    print_warning(" ffmpeg finished with exit code: %d. Most probably something went wrong." % (exit_code))