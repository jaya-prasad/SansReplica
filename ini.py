'''
	Author : pakhandi

	The program is aimed on creating a directory of unique images from a given source directory.
	The program should be able to identify two images as similar even after slight modification to one of them.

'''

from PIL import Image
import os
import shutil
from collections import defaultdict
import sys

#Function to get Hamming Distance between two strings
def hammingDistance(s1, s2):
    if len(s1) != len(s2):
    	return 100
    return sum(bool(ord(ch1) - ord(ch2)) for ch1, ch2 in zip(s1, s2))

#Function to check if a file is of supported format or not
def is_image_file(f):
	return f.lower().endswith(('.png', '.jpg', '.jpeg'))

#Function to get the hash value of an image
def get_hash(f):
	img = Image.open(f)
	img = img.resize((8, 8), Image.ANTIALIAS)
	img = img.convert("L")

	pixels = list(img.getdata())
	avg = sum(pixels) / len(pixels)

	bits = "".join(map(lambda pixel: '1' if pixel < avg else '0', pixels));
	hexadecimal = int(bits, 2).__format__('016x').upper()

	return hexadecimal

#Included command line arguments
if len(sys.argv)!=3:
	print "Error !!! Correct usage : python ini.py <Directory for images> <Directory for uniques>"
	exit()

#Removing "/" from the end of the source directory
if sys.argv[1].endswith('/'):
	sys.argv[1] = sys.argv[1][:-1]

#Adding "/" at the end of the destination directory
if sys.argv[2].endswith('/') == 0:
	sys.argv[2] = sys.argv[2] + "/"

hash_value = {}
similar_file_list = defaultdict(list)
files = [f for f in os.listdir(sys.argv[1])]
files = [sys.argv[1] + f for f in files]

#Iterating through all the folders recursively
for root, dirs, files in os.walk(sys.argv[1]):
	for file in files:
		f = root+"/"+file
		x = f
		if not is_image_file(x):
			continue
		hash_value[f] = get_hash(f)
		#Image and it's hash
		print f," --> ",hash_value[f]

for f in sorted(hash_value):
	for x in sorted(hash_value):
		if(hammingDistance(hash_value[f],hash_value[x])<2 and f!=x):
			if f < x:
				similar_file_list[f].append(x)
			else:
				similar_file_list[x].append(f)
			#Pair of images and their hammingDistance
			print f," --> ",x," <",hammingDistance(hash_value[f],hash_value[x]),">"

unique_files = 0;

for f in sorted(hash_value):
	flag = 1
	fn = f.rsplit("/")
	fn = fn[len(fn)-1]
	for x in similar_file_list:
		for y in similar_file_list[x]:
			if f == y:
				flag = 0
				break
		if flag == 0:
			break
	if flag == 1:
		if not os.path.exists(sys.argv[2]):
			os.makedirs(sys.argv[2])
		shutil.copyfile(f,sys.argv[2]+fn)
		unique_files = unique_files + 1

print unique_files," files were found unique"
