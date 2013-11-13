#!/bin/python

import subprocess
import os
from PIL import Image

'''
SORT PDFs BY BRIGHTNESS
Jeff Thompson | 2013 | www.jeffreythompson

Experiment in auto-curating for a residency with Internet Archive: all PDFs with mention
of the word "brigthness", sorted by brightness.

BRIGHTNESS MEASURE:
via: http://stackoverflow.com/a/596243/1167783
+		standard, objective: (0.2126*R) + (0.7152*G) + (0.0722*B)
+		perceived, option 1: (0.299*R + 0.587*G + 0.114*B)
+		perceived, option 2, slower to calculate: sqrt(0.241*R^2 + 0.691*G^2 + 0.068*B^2)

IMAGE EXPORT SETTINGS:
+		density - sets resolution; we downsample to save space
+		background - prevents images from having transparent backgrounds (default)

REQUIRES:
+		ImageMagick
+		Ghostscript

TO DO/IDEAS:
+		

'''

split_pdfs = False

input_dir = "InputPDFs/"
output_dir = "SplitPNGs/"
csv_file = "brightness.csv"


# create output directory if it doesn't exist
def create_dir(path):
	if not os.path.exists(path):
		os.makedirs(path)


# get first color pdf in the directory (not ending with '_bw')
def get_first_pdf(id):
	for file in os.listdir(input_dir + id):
		if file.endswith(".pdf") and not file.endswith("_bw.pdf"):
			return file


def get_image_brightness(path):
	print "  " + path
	brightness = 0.0
	img = Image.open(path)
	img = img.convert("RGB")	# required for comparison
	width, height = img.size
	if width == 0 or height == 0:
		return 0.0
	for y in range(height):
		for x in range(width):
			r, g, b = img.getpixel((x,y))
			brightness += (0.2126 * r) + (0.7152 * g) + (0.0722 * b)
	return(brightness/(width * height))


# clear terminal window first :)
os.system('cls' if os.name=='nt' else 'clear')


# write header to csv file
with open(csv_file, 'a') as csv:
	csv.write('id,brightness,url')


# iterate pdfs and split into png files
if split_pdfs:
	for id in os.listdir(input_dir):
		if not id.startswith('.'):
			create_dir(output_dir + id)		
			pdf = get_first_pdf(id)
			print id + "/" + pdf
			print "  splitting into PNG files...\n"
			subprocess.call(["convert", "-density", "72", "-background", "white", input_dir + "/" + id + "/" + pdf, output_dir + id + "/%04d.png"])


# iterate all pngs, calculate average brightness
for id in os.listdir(output_dir):
	if not id.startswith('.'):
		
		# list all pngs in the folder, extract overall brightness for pdf
		print id
		brightness = 0.0
		num_images = 0
		for png in os.listdir(output_dir + id):
			if png.endswith('.png'):
				brightness += get_image_brightness(output_dir + id + "/" + png)
				num_images += 1
		if num_images == 0:
			continue
		brightness /= num_images
		url = '<a href="http://www.archive.org/details/' + id + '">link</a>'
		
		with open(csv_file, 'a') as csv:
			csv.write('\n' + id + ',' + str(brightness) + ',' + url)
		print "brightness: " + str(brightness) + "\n"
