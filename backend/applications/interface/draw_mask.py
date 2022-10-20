import cv2
import numpy as np


def draw_masks(img_path):
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)
    count = len(contours)  #变化区域个数
    img = np.ones((img.shape[0], img.shape[1], 4)) * (255, 255, 255, 0)
    img = cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
    b = img[:, :, 0]
    g = img[:, :, 1]
    r = img[:, :, 2]
    a = img[:, :, 3]
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if not (b[i][j] > 0 and g[i][j] > 0 and r[i][j] > 0):
                a[i][j] = 255  # 255不透明，0全透明，有像素的地方设置不透明
    mask = cv2.merge((b, g, r, a))
    return mask, count
