from PyQt5.QtWidgets import *
import cv2
import numpy as np
import winsound
import sys


class Panorama(QMainWindow):
    def __init__(self):
        super().__init__()
        self.fail_cnt = 0
        self.setWindowTitle("파노라마 영상")
        self.setGeometry(400, 400, 800, 200)

        collectButton = QPushButton("영상 수집", self)
        self.showButton = QPushButton("영상 보기", self)
        self.stitchButton = QPushButton("봉합", self)
        self.saveButton = QPushButton("저장", self)
        quitButton = QPushButton("나가기", self)
        self.label = QLabel("환영합니다!", self)

        collectButton.setGeometry(10, 25, 140, 70)
        self.showButton.setGeometry(160, 25, 140, 70)
        self.stitchButton.setGeometry(310, 25, 140, 70)
        self.saveButton.setGeometry(460, 25, 140, 70)
        quitButton.setGeometry(650, 25, 140, 70)
        self.label.setGeometry(10, 70, 600, 170)

        self.showButton.setEnabled(False)
        self.stitchButton.setEnabled(False)
        self.saveButton.setEnabled(False)

        collectButton.clicked.connect(self.collectFunction)
        self.showButton.clicked.connect(self.showFunction)
        self.stitchButton.clicked.connect(self.stitchFunction)
        self.saveButton.clicked.connect(self.saveFunction)
        quitButton.clicked.connect(self.quitFunction)

    def collectFunction(self):
        self.showButton.setEnabled(False)
        self.stitchButton.setEnabled(False)
        self.saveButton.setEnabled(False)
        self.label.setText("\nc를 여러 번 눌러 수집하고 끝나면\nq를 눌러 비디오를 끕니다.")

        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            sys.exit("카메라 연결 실패")

        self.imgs = []
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            cv2.imshow("video display", frame)

            key = cv2.waitKey(1)
            if key == ord("c"):
                self.imgs.append(frame)  # 영상 저장
            elif key == ord("q"):
                self.cap.release()
                cv2.destroyWindow("video display")
                break

        if len(self.imgs) >= 2:  # 수집한 영상이 2장 이상이면
            self.showButton.setEnabled(True)
            self.stitchButton.setEnabled(True)
            self.saveButton.setEnabled(True)

    def showFunction(self):
        self.label.setText("수집된 영상은 " + str(len(self.imgs)) + "장 입니다.")
        stack = cv2.resize(self.imgs[0], dsize=(0, 0), fx=0.25, fy=0.25)
        for i in range(1, len(self.imgs)):
            stack = np.hstack(
                (stack, cv2.resize(self.imgs[i], dsize=(0, 0), fx=0.25, fy=0.25))
            )
        cv2.imshow("Image collection", stack)

    def stitchFunction(self):
        stitcher = cv2.Stitcher_create()
        status, self.img_stitched = stitcher.stitch(self.imgs)
        if status == cv2.STITCHER_OK:
            cv2.imshow("Image stitched panorama", self.img_stitched)
            self.label.setText("파노라마 제작에 성공했습니다.")
            self.fail_cnt = 0
        else:
            self.fail_cnt += 1
            winsound.Beep(3000, 500)
            self.label.setText(f"파노라마 제작에 실패했습니다. 다시 시도하세요.\n(실패 횟수: {self.fail_cnt}회)")

    def saveFunction(self):
        fname = QFileDialog.getSaveFileName(self, "파일 저장", "./", "Images (*.png *.jpg *.bmp)")
        cv2.imwrite(fname[0], self.img_stitched)

    def quitFunction(self):
        self.cap.release()
        cv2.destroyAllWindows()
        self.close()


app = QApplication(sys.argv)
win = Panorama()
win.show()
app.exec_()