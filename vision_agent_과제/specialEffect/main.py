import cv2
import numpy as np
from PyQt5.QtWidgets import *
import sys


class SpecialEffect(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("사진 특수 효과")
        self.setGeometry(400, 600, 760, 350)

        pictureButton = QPushButton("사진 읽기", self)
        embossButton = QPushButton("엠보싱", self)
        cartoonButton = QPushButton("카툰", self)
        sketchButton = QPushButton("연필 스케치\n(명암)", self)
        sketchButton_2 = QPushButton("연필 스케치\n(컬러)", self)
        oilButton = QPushButton("유화", self)
        saveButton = QPushButton("저장하기", self)
        self.pickCombo = QComboBox(self)
        self.pickCombo.addItems(["엠보싱", "카툰", "연필 스케치(명암)", "연필 스케치(컬러)", "유화"])
        quitButton = QPushButton("나가기", self)
        self.label = QLabel("환영합니다! 사진을 선택해주세요", self)
        self.label_2 = QLabel("미리보기", self)


        pictureButton.setGeometry(10, 25, 140, 70)
        embossButton.setGeometry(10, 160, 140, 70)
        cartoonButton.setGeometry(160, 160, 140, 70)
        sketchButton.setGeometry(310, 160, 140, 70)
        sketchButton_2.setGeometry(460, 160, 140, 70)
        oilButton.setGeometry(610, 160, 140, 70)
        self.pickCombo.setGeometry(160, 25, 140, 70)
        saveButton.setGeometry(310, 25, 140, 70)
        quitButton.setGeometry(610, 25, 140, 70)
        self.label.setGeometry(10, 240, 500, 170)
        self.label_2.setGeometry(10, 50, 500, 170)

        pictureButton.clicked.connect(self.pictureOpenFunction)
        embossButton.clicked.connect(self.embossFunction)
        cartoonButton.clicked.connect(self.cartoonFunction)
        sketchButton.clicked.connect(self.sketchFunction)
        sketchButton_2.clicked.connect(self.sketchFunction_2)
        oilButton.clicked.connect(self.oilFunction)
        saveButton.clicked.connect(self.saveFunction)
        quitButton.clicked.connect(self.quitFunction)

    def pictureOpenFunction(self):
        fname = QFileDialog.getOpenFileName(self, "사진 읽기", "./")
        self.img = cv2.imread(fname[0])
        if self.img is None:
            sys.exit("파일을 찾을 수 없습니다.")

        cv2.imshow("Painting", self.img)

    def embossFunction(self):
        self.emboss = np.array([[-1.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 1.0]])

        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        gray16 = np.int16(gray)
        self.emboss = np.uint8(np.clip(cv2.filter2D(gray16, -1, self.emboss) + 128, 0, 255))

        cv2.imshow("Emboss", self.emboss)

    def cartoonFunction(self):
        self.cartoon = cv2.stylization(self.img, sigma_s=60, sigma_r=0.45)
        cv2.imshow("Cartoon", self.cartoon)

    def sketchFunction(self):
        self.sketch_gray, self.sketch_color = cv2.pencilSketch(
            self.img, sigma_s=60, sigma_r=0.07, shade_factor=0.02
        )
        cv2.imshow("Pencil sketch(gray)", self.sketch_gray)
        
    def sketchFunction_2(self):
        self.sketch_gray, self.sketch_color = cv2.pencilSketch(
            self.img, sigma_s=60, sigma_r=0.07, shade_factor=0.02
        )
        cv2.imshow("Pencil sketch(color)", self.sketch_color)

    def oilFunction(self):
        self.oil = cv2.xphoto.oilPainting(self.img, 10, 1, cv2.COLOR_BGR2Lab)
        cv2.imshow("Oil painting", self.oil)

    def saveFunction(self):
        fname = QFileDialog.getSaveFileName(self, "파일 저장", "./", "Image Files (*.png *.jpg *.jpeg *.bmp *.tiff)")
        i = self.pickCombo.currentIndex()
        
        if i == 0:
            cv2.imwrite(fname[0], self.emboss)
        elif i == 1:
            cv2.imwrite(fname[0], self.cartoon)
        elif i == 2:
            cv2.imwrite(fname[0], self.sketch_gray)
        elif i == 3:
            cv2.imwrite(fname[0], self.sketch_color)
        elif i == 4:
            cv2.imwrite(fname[0], self.oil)
            
        self.label.setText("파일이 저장되었습니다.")


    def quitFunction(self):
        cv2.destroyAllWindows()
        self.close()

app = QApplication(sys.argv)
win = SpecialEffect()
win.show()
app.exec_()