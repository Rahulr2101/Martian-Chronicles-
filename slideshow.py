import requests
from PIL import Image
import urllib
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

from PySide6 import QtCore
import sys
 
 
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
 
        # app title
        self.setWindowTitle("Martian-Chronicles")
 
        #  window       (left,top,width,height)
        self.setGeometry(100, 100, 1920, 1080)
        self.UiComponents()
 
        
        self.show()
    
        

 

    def UiComponents(self):
        #image code 

        self.SolLabel = QLabel(self)
        self.SolLabel.setText('Earth_date:')
        self.SolLabel.move(1420, 200)

        self.Solinput = QLineEdit(self)
        self.Solinput.move(1500, 200)
        self.Solinput.resize(280,40)

        self.CameraLabel = QLabel(self)
        
        self.CameraLabel.setText('Camera:')
        self.CameraLabel.move(1440,250)

        self.Camerainput = QLineEdit(self)
        self.Camerainput.move(1500, 250)
        self.Camerainput.resize(280,40)
        
        self.PageLabel = QLabel(self)
        self.PageLabel.setText('Page:')
        self.PageLabel.move(1455,300)

        self.Pageinput = QLineEdit(self)
        self.Pageinput.move(1500, 300)
        self.Pageinput.resize(280,40)



        self.label = QLabel(self)




        button = QPushButton("Fetch Image", self)
        button.setGeometry(1650, 400, 100, 30)
    





    
        fow = QPushButton(">", self)
        fow.setGeometry(1000, 500, 30, 30)
        fow.setStyleSheet("background-color: transparent;")

        fow.clicked.connect(self.foward)

        back = QPushButton("<", self)
        back.setGeometry(10, 500, 30, 30)
        back.setStyleSheet("background-color: transparent;")

        back.clicked.connect(self.back)
        self.num = 0
        self.index = 0



        #code for color
        # button.setStyleSheet("color : rgba(0, 0, 0, 100)")

        button.clicked.connect(self.Fetch_data)
 
    # action method
    def Fetch_data(self):
        input1 = self.Solinput.text()
        input2 = self.Camerainput.text()
        input3 = self.Pageinput.text() 
        print(input1,input2,input3)

        req = requests.get(f"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol={input1}&camera={input2}&page={input3}&api_key=5SmFOsZLd2pZod4q3aaBn0s0mGQg88B8iTG9y5WV").json()
        photo_lst =[]
        for i in req['photos']:
            self.num += 1 
            urllib.request.urlretrieve(f"{i['img_src']}",f"photo{self.num}.jpg")
            photo_lst.append(f"photo{self.num}.jpg")
        print("number = ", self.num)
        print("pressed")
        self.index += 1
        pixmap = QPixmap(f"photo{self.index}.jpg")
        self.label.resize(pixmap.width(), pixmap.height())
        self.label.setPixmap(pixmap)
        self.label.show()



    def foward(self):
        if self.index <= self.num-1:
            self.index += 1
            print(self.index)

            pixmap = QPixmap(f"photo{self.index}.jpg")
            self.label.resize(pixmap.width(), pixmap.height())
            self.label.setPixmap(pixmap)
            self.label.show()
        else:
            self.index = 1
            pixmap = QPixmap(f"photo{self.index}.jpg")
            self.label.resize(pixmap.width(), pixmap.height())
            self.label.setPixmap(pixmap)
            self.label.show()
    
    def back(self):
        if self.index >= 0:
            self.index -= 1
            print(self.index)
            pixmap = QPixmap(f"photo{self.index}.jpg")
            self.label.resize(pixmap.width(), pixmap.height())
            self.label.setPixmap(pixmap)
            self.label.show()
        else:
            self.index = self.num 
            print(self.index)
            pixmap = QPixmap(f"photo{self.index}.jpg")
            self.label.resize(pixmap.width(), pixmap.height())
            self.label.setPixmap(pixmap)
            self.label.show()


       

 

App = QApplication(sys.argv)
 
window = Window()
indx = 0

sys.exit(App.exec())