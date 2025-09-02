import os
import cv2
images = [os.path.join('images',image) for image in os.listdir('images') if image.endswith('.jpg')]
for image_path in images:
    image = cv2.imread(image_path)
    if image is not None:
        resized_image = cv2.resize(image, (640, 640))
        cv2.imwrite(image_path, resized_image)
    else:
        print(f"Failed to read image: {image_path}")