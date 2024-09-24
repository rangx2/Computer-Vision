import cv2

cap = cv2.VideoCapture("./assets/video.mp4")
if not cap.isOpened(): # 보통은 boolean 값 반환
    sys.exit("파일 없음")
    
captures = []
    
while True:
    ret, frame = cap.read()
    if ret:
        cv2.imshow("비디오", frame)
        key = cv2.waitKey(1)
        if key == ord("c"):
            captures.append(frame)
            print(captures)
        elif key == ord("q"):
            break
    
cap.release()
cv2.destroyAllWindows()

# 캡쳐된 프레임 저장하기
if len(captures) > 0:
    for i, capture in enumerate(captures):
        cv2.imwrite(f"./outputs/frame-{i}.jpg", capture)
