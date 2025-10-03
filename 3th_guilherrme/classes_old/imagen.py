import numpy as np
import matplotlib.pyplot as plt
import cv2
img = cv2.imread('peixe.png')

rgb = cv2.resize(img, (20, 20), interpolation=cv2.INTER_NEAREST)
print(rgb)

plt.imshow(rgb)
plt.axis('off')
plt.show()
