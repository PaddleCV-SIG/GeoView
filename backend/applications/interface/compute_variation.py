import cv2
import numpy as np


def compute_variation(img_path):
    img = cv2.imread(img_path)
    changed_area = np.sum(img == 255)
    unchanged_area = np.sum(img == 0)
    fractional_variation = (changed_area /
                            (changed_area + unchanged_area)) * 100
    return fractional_variation
