import glob
import os
import os.path
from subprocess import call

def get_video_parts(video_path):
	parts = video_path.split(os.path.sep)
	filename = parts[2]
	filename_no_ext = filename.split('.')[0]
	classname = parts[1]
	train_or_test = parts[0]

	return train_or_test, classname, filename_no_ext, filename


data_file = []
folders = ['train', 'test']

for folder in folders:
	class_folders = glob.glob(os.path.join(folder, '*'))

	for vid_class in class_folders:
		class_files = glob.glob(os.path.join(vid_class, '*.mp4'))
		k=0
		for video_path in class_files:

			video_parts = get_video_parts(video_path)

			train_or_test, classname, filename_no_ext, filename = video_parts

			dest = os.path.join(train_or_test, classname,"a", filename_no_ext + '-%d'+ '.mp4')

			print(dest)
			call(["ffmpeg", "-i", video_path, "-acodec", "copy","-f" , "segment", "-segment_time", "10", "-vcodec", "copy" ,"-reset_timestamps", "1", "-map", "0", "-an", dest])
			# Get the parts of the file.

 #ffmpeg -i test.mp4 -acodec copy -f segment -segment_time 2 -vcodec copy -reset_timestamps 1 -map 0 -an split_test_%d.mp4