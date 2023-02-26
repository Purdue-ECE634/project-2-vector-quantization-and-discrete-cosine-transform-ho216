# -*- coding: utf-8 -*-
"""Project2_VQ.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1diLYMte6GAT3cj8Xzc3QKAiGBivuvhmI
"""

from google.colab import drive
import glob
drive.mount('/content/drive')

import argparse
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pdb
from math import sqrt, log10
import glob

parser = argparse.ArgumentParser("Vector Quantization")
parser.add_argument("-p", "--path", required=True, help="train image path")
parser.add_argument("-l", "--level", required=True, help="quantization level")
parser.add_argument("-i", "--image_path", type=str, required=True, help="input path")
args = parser.parse_args()

path = args.path
level = args.level
image_path = args.image_path

# path = '/content/drive/MyDrive/sample_image/training/*'
# # path = '/content/drive/MyDrive/sample_image/training/boat.png'
# image_path = '/content/drive/MyDrive/sample_image/training/boat.png'
# level = '256'

def mse(x, y):
	return np.mean((x - y) ** 2)
 
def PSNR(x, y):
	mse_value = mse(x, y)
	psnr = 20 * log10(255.0 / sqrt(mse_value))
	return psnr

def quantization(book, image):
	H, W = np.shape(image)
	output = np.zeros((H, W))

	for i in range(H//4):
		for j in range(W//4):
			block = image[(4*i) : (4*(i+1)), (4*j) : (4*(j+1))]
			mse_max = np.inf
			for k in range(book.shape[0]):
				mse_value = mse(block, book[k])
				if mse_value < mse_max:
					mse_max = mse_value
					level = k
			output[(4*i) : (4*(i+1)), (4*j) : (4*(j+1))] = book[level]
	plt.imshow(output, cmap='gray')
	return output

train_data = []
for image in glob.glob(path):
  img = cv2.imread(image, 0)
  H, W = np.shape(img)
  for i in range(H//4):
    for j in range(W//4):
      temp = img[(4*i):(4*(i+1)), (4*j):(4*(j+1))]
      train_data.append(temp)


level = int(level)
total_train_data = len(train_data)
book = np.arange(0, 256, 256 // level).reshape((level, 1))

book = np.tile(book, 16).reshape((level, 4, 4))
train_data = np.asarray(train_data)

iteration_count = 0
while iteration_count < 100:
  codevec = np.zeros((total_train_data))
  errvec = np.zeros((total_train_data))
  print(iteration_count)
  for i in range(total_train_data):
    mse_best = np.inf
    for j in range(level):
      mse_value = mse(train_data[i], book[j])
      if mse_value < mse_best:
        mse_best = mse_value
        code = j
    codevec[i] = code
    errvec[i] = mse_best
  D1 = np.mean(errvec)

  if iteration_count == 0 or (np.abs(D1 - D0) / D0) >= 0.01:
    for l in range(level):
      if np.sum(codevec == l) == 0: book[l] = np.zeros((4, 4))
      else: book[l] = np.mean(train_data[codevec == l], axis=0)
    D0 = D1
    iteration_count += 1
  else: break

test_image = cv2.imread(image_path, 0)
plt.imshow(test_image, cmap='gray')

quantization_image = quantization(book, test_image)
psnr = PSNR(test_image, quantization_image)
print(psnr)

