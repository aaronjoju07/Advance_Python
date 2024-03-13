import numpy as np
import cv2 as cv

img = np.zeros((512, 512, 3), np.uint8)

cv.rectangle(img, (0, 0), (100, 100), (180, 255, 14), 10)
cv.rectangle(img, (100, 100), (200, 200), (180, 220, 1), 3)
cv.rectangle(img, (200, 200), (300, 300), (180, 205, 5), 3)
cv.rectangle(img, (300, 300), (400, 400), (80, 255, 10), 3)
cv.rectangle(img, (400, 400), (512, 512), (80, 255, 10), 3)

font = cv.FONT_HERSHEY_SIMPLEX
cv.putText(img, 'AARON', (150, 50), font, 1, (255, 255, 255), 2, cv.LINE_AA)

cv.imshow('Image with Square and Name', img)
cv.waitKey(0)
cv.destroyAllWindows()
