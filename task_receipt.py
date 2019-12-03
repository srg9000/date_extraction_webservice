# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 14:33:12 2019

@author: srg
"""
import copy
import cv2
import numpy as np
import os
import pytesseract
from pytesseract import image_to_string
from PIL import Image
import tempfile
from task_translation import date_forms

pytesseract.pytesseract.tesseract_cmd = './.apt/usr/share/tesseract-ocr/4.00/tessdata'
# increase image dpi
def set_image_dpi(file_path):
	''' set image dpi to 1000 '''
	im = Image.open(file_path)
	length_x, width_y = im.size
	factor = min(1, float(1024.0 / length_x))
	size = int(factor * length_x), int(factor * width_y)
	im_resized = im.resize(size, Image.ANTIALIAS)
	temp_file = tempfile.NamedTemporaryFile(delete=False,   suffix='.png')
	temp_filename = temp_file.name
	im_resized.save(temp_filename, dpi=(1000, 1000))
	return temp_filename


# unsharp mask method of image sharpening
def unsharp_mask(image, kernel_size=(5, 5), sigma=4.5, amount=3.0, threshold=100):
	''' Return a sharpened version of the image, using an unsharp mask '''
	blurred = cv2.GaussianBlur(image, kernel_size, sigma)
	sharpened = float(amount + 1) * image - float(amount) * blurred
	sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
	sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
	sharpened = sharpened.round().astype(np.uint8)
	if threshold > 0:
		low_contrast_mask = np.absolute(image - blurred) < threshold
		np.copyto(sharpened, image, where=low_contrast_mask)
	return sharpened


# function that will extract date
def extract_date(img_src):
	''' preprocess, OCR and date extraction '''
	temp = set_image_dpi(img_src)
	img = cv2.imread(temp)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	# Reducing shadows and other effects by subtracting dialated and blurred
	# image
	dilated_img = cv2.dilate(img, np.ones((11, 11), np.uint8))
	bg_img = cv2.medianBlur(dilated_img, 21)
	diff_img = 255 - cv2.absdiff(img, bg_img)
	norm_img = diff_img.copy()
	
	# minmax normalization
	cv2.normalize(diff_img, norm_img, alpha=0, beta=255,
				  norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
	_, img = cv2.threshold(norm_img, 255, 0, cv2.THRESH_TRUNC)
	cv2.normalize(img, img, alpha=0, beta=255,
				  norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
	
	# image sharpening
	sharp = unsharp_mask(img)

	# ocr with pytesseract, --psm 6 = Image considered as bulk/paragraph text,
	# --oem 3 = OCR engine(LSTM based)
	strn = image_to_string(sharp, lang='eng', config='--psm 6 --oem 3')
	
	# extract date from teext using regex and datefinder library
	response = date_forms(strn)
    # print(strn)
	return response
