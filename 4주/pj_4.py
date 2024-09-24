import cv2
import sys

img = cv2.imread("./cat2.jpg")
if img is None:
    sys.exit("파일을 찾을 수 없습니다.")
    
svt_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    
cv2.imshow("pj_4 Gray",svt_img)
cv2.waitKey()
cv2.destroyAllWindows()
