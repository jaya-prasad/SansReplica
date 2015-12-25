from PIL import Image
import os
import shutil
from collections import defaultdict

def hammingDistance(s1, s2):
    """Return the Hamming distance between equal-length sequences"""
    if len(s1) != len(s2):
    	return 100
        raise ValueError("Undefined for sequences of unequal length")
    return sum(bool(ord(ch1) - ord(ch2)) for ch1, ch2 in zip(s1, s2))

d = {}
felim = defaultdict(list)
files = [f for f in os.listdir("aich/")]
files = ["aich/" + f for f in files]

for f in files:

	x = f

	if x.lower().endswith(('.png', '.jpg', '.jpeg')) == 0:
		continue

	img = Image.open(f)
	img = img.resize((8, 8), Image.ANTIALIAS)

	img = img.convert("L")

	pixels = list(img.getdata())
	avg = sum(pixels) / len(pixels)

	#print f,avg
	
	bits = "".join(map(lambda pixel: '1' if pixel < avg else '0', pixels));
	hexadecimal = int(bits, 2).__format__('016x').upper()

	print f," ",hexadecimal
	d[f] = hexadecimal

dr = 0

for f in sorted(d):
	for x in sorted(d):
		if(hammingDistance(d[f],d[x])<2 and f!=x):
			if f < x:
				felim[f].append(x)
			else:
				felim[x].append(f)
			print f," --> ",x," <",hammingDistance(d[f],d[x]),">"

for f in felim:
	print f

for f in sorted(d):
	flag = 1
	fn = f.rsplit("/")
	fn = fn[len(fn)-1]
	for x in felim:
		for y in felim[x]:
			if f == y:
				flag = 0
				break
		if flag == 0:
			break
	if flag == 1:
		shutil.copyfile(f,"aich/temp/"+fn)
