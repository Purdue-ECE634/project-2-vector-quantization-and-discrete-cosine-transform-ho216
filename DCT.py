# -*- coding: utf-8 -*-
"""Project2_DCT.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1sdJrekXAOcwN_usq4hWyFpoLcLHIL6tr
"""

from google.colab import drive
import glob
drive.mount('/content/drive')

import argparse
import os
import cv2
import numpy as np
import pdb
from math import sqrt, log10
import glob
from scipy.fftpack import dct, idct
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser("DCT")
parser.add_argument("-i", "--image_path", type=str, required=True, help="input path")
parser.add_argument("-k", "--K", required=True, help="K value")
args = parser.parse_args()

image_path = args.image_path
K = args.K

# path = '/content/drive/MyDrive/sample_image/training/*'
# path = '/content/drive/MyDrive/sample_image/training/monarch.png'
# image_path = '/content/drive/MyDrive/sample_image/training/airplane.png'
# K = '2'

def mse(x, y):
	return np.mean((x - y) ** 2)
 
def PSNR(x, y):
	mse_value = mse(x, y)
	psnr = 20 * log10(255.0 / sqrt(mse_value))
	return psnr

def DCT(block):
  result = dct(dct(block, axis=0, norm='ortho'), axis=1, norm='ortho')
  return result

def IDCT(block):
  result = idct(idct(block, axis=0, norm='ortho'), axis=1, norm='ortho')
  return result

def compute_coeff(block, K):
  H, W = block.shape
  result = np.zeros_like(block)	
  row, column, direction = 0, 0, 0

  for k in range(K):
    result[row, column] = block[row, column]
    if direction == 0:
      if k == 0: column, direction = (column+1), 3
      else: row, column, direction = (row+1), (column-1), 3
  
    elif direction == 1:
      if row == (H-1): column, direction = (column+1), 0
      elif column == (W-1): row, column, direction = (row+1), (column-1), 3
      else: row, column, direction = (row-1), (column+1), 2

    elif direction == 2:
      if row == 0: column, direction = (column+1), 0
      elif column == (W-1): row, direction = (row+1), 1
      else: row, column, direction = (row-1), (column+1), 2

    elif direction == 3:
      if column == 0: row, direction = (row+1), 1
      else: row, column, direction = (row+1), (column-1), 3	

  return result

test_image = cv2.imread(image_path, 0)
plt.imshow(test_image, cmap='gray')
K = int(K)
dct_image = np.zeros_like(test_image)
H, W = np.shape(test_image)

for i in range(H//8):
  for j in range(W//8):
    block = test_image[(8*i) : (8*(i+1)), (8*j) : (8*(j+1))]
    dct_block = DCT(block)
    temp_block = compute_coeff(dct_block, K)
    dct_image[(8*i) : (8*(i+1)), (8*j) : (8*(j+1))] = IDCT(temp_block)

plt.imshow(dct_image, cmap='gray')
psnr = PSNR(test_image, dct_image)
print(psnr)

