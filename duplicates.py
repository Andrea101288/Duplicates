import os
import cv2
import numpy as np
import shutil
import glob
from os import path
from shutil import copyfile, copy 

# Define Class
class Images_finder:	
	
	# define method to get the source folder path
	def get_src_folder_path(self):
			# asking for an input until you write a correct existing path
			while True:
				rootdir = input("Insert source directory where you want to find the duplicate images\n")
				if '"' in rootdir:
					rootdir = rootdir.replace('"', '')
				if(path.exists(rootdir) is False):
					print("Wrong path, the folder path doesn't exist..")	
				if(path.exists(rootdir) is True):  
					break  
			return rootdir
	
	# define method to get the destination folder path
	def get_dst_folder_path(self):
			while True:
				rootdir = input("Insert destination directory where you want to move the duplicate images to check them\n")
				if '"' in rootdir:
					rootdir = rootdir.replace('"', '')
				if(path.exists(rootdir) is False):
					print("Wrong path, the folder path doesn't exist..")
				# if path exists	
				if(path.exists(rootdir) is True):  
					break  
			return rootdir	
			
	# define method to get file extentions
	def get_ext(self):
	
		while True:
			ext = input("Insert image extention you want to look for (png, jpg or jpeg)\n")
			if(ext == "jpg" or ext == "jpeg" or ext == "png"):
				break
			else:
				print("Wrong extention inserted!\n")
				
		return ext
        
	# define method to store the images into an array
	def store_images(self, src_dir, ext):
	
		pictures = []
		# searching recursively files you are looking for
		path = os.path.normpath('%s/**/*.'+ext)
		for file in glob.iglob(os.path.normpath(path % src_dir), recursive=True):
			width = 600
			height = 600
			dim = (width, height)
			# resizing images 600 x 600
			resized_image = cv2.resize(cv2.imread(file), dim, interpolation = cv2.INTER_AREA)
			# dictionary creation with name, path and image 
			curr_pic = {			
				'name': os.path.basename(file),
				'path': file,
				'image': resized_image
			}
			# add dictionary to the array
			pictures.append(curr_pic)
			
		return pictures		
	
	# define method find_images
	def find_images(self, image_list, dst_folder):	
		image_dulplicates = 0		
		for i in range(0, len(image_list)):
			curr = image_list[i]['image']
			for j in range(i+1, len(image_list)):
				next = image_list[j]['image']	
				# calculate the difference between the 2 images
				difference = cv2.subtract(curr, next) 		
				result = not np.any(difference)
				if result is True:	
					dir = dst_folder+"/"+image_list[i]['name']
					# if it doesn't exist yet create a folder to put the 2 images to check them
					if path.exists(dir) is False:
						os.mkdir(dir)
						copyfile(os.path.normpath(image_list[i]['path']), os.path.normpath(dir+"/"+image_list[i]['name']))
					image_dulplicates +=1	
					# delete de duplicate from the source folder and move it
					shutil.move(image_list[j]['path'], os.path.normpath(dir+"/"+image_list[j]['name']))	
					print("picture "+ image_list[i]['name'] + " and picture " + image_list[j]['name'] +" are the same\n")
				else:
					break
					
		return image_dulplicates			

# Main function					
if __name__ == "__main__":

	Duplicates = Images_finder()
	src_folder = Duplicates.get_src_folder_path()
	dst_folder = Duplicates.get_dst_folder_path()
	ext = Duplicates.get_ext()
	image_list = Duplicates.store_images(src_folder, ext)
	number_duplicate_images = Duplicates.find_images(image_list, dst_folder)
	if(len(image_list) > 0):
		print("Checking complete! Total "+ext+" files found : "+str(len(image_list))+"\n"+str(number_duplicate_images)+" equal images found" )
	else:
		print("No "+ext+" files found..")
	