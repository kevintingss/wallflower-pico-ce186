# import glob
# import os
#
# gif_name = 'outputName'
# file_list = glob.glob('*.png') # Get all the pngs in the current directory
# list.sort(file_list, key=lambda x: int(x.split('p')[1].split('.')[0])) # Sort the images by #, this may need to be tweaked for your use case
#
# with open('image_list.txt', 'w') as file:
#     for item in file_list:
#         file.write("%s\n" % item)
#
# os.system('convert @image_list.txt {}.gif'.format(gif_name)) # On windows convert is 'magick'

import glob
import moviepy.editor as mpy

gif_name = 'outputName'
fps = 1
file_list = glob.glob('*.png') # Get all the pngs in the current directory
list.sort(file_list, key=lambda x: int(x.split('p')[1].split('.')[0])) # Sort the images by #, this may need to be tweaked for your use case
clip = mpy.ImageSequenceClip(file_list, fps=fps)
clip.write_gif('{}.gif'.format(gif_name), fps=fps)