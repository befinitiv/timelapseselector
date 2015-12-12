import numpy
import os
import math
import scipy.misc
import scipy.ndimage
import matplotlib.pyplot as plt

INP_DIR='motion' #folder of the input files
OUTP_DIR='sel' #folder (must be existent) of the output symbolic links
PICS_PER_DAY=48 #how many pictures have you shot per day?
START_IMAGE=25 #this is your manually selected initial image from the first day

images = sorted(os.listdir(INP_DIR))

def open_img(index):
	return scipy.misc.imread(INP_DIR+'/'+images[index])

#score is just a sum of absolute differences
def compare_score(img0, img1):
	return numpy.sum(numpy.abs(img0.astype(numpy.int16)-img1.astype(numpy.int16)))

#low-pass filter each color channel
def prefilter(img):
	SIGMA=5
	return numpy.dstack((scipy.ndimage.gaussian_filter(img[:,:, 0], sigma=SIGMA), scipy.ndimage.gaussian_filter(img[:,:, 1], sigma=SIGMA), scipy.ndimage.gaussian_filter(img[:,:, 2], sigma=SIGMA)))

def find_best_image_of_day(ref_idx, start_idx):
	ref_img = open_img(ref_idx)
	ref_img_pref = prefilter(ref_img)

	print 'Finding best candidate for %d: %s...' % (ref_idx, images[ref_idx])
	scores = []
	for i in range(start_idx, start_idx+PICS_PER_DAY):
		cmp_img = open_img(i)
		cmp_img_pref = prefilter(cmp_img)

		score = compare_score(ref_img_pref, cmp_img_pref)
		scores.append(score)
		print '%d\t%s : %d' % (i, images[i], score)
	
	best = numpy.argmin(scores) + start_idx
	print 'Selecting %s' % images[best]
	return best

curr_ref = START_IMAGE
while curr_ref+PICS_PER_DAY < len(images):
	os.symlink('../' + INP_DIR + '/' + images[curr_ref], OUTP_DIR+'/'+images[curr_ref])
 
 	start_of_next_day = int(math.ceil(float(curr_ref) / PICS_PER_DAY) * PICS_PER_DAY)
 	curr_ref = find_best_image_of_day(curr_ref, start_of_next_day)
