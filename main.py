
import requests
import urllib
import shutil
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6 import QtCore
import time
import sys
import smtplib
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

class FetchThread(QThread):
    fetch_signal = QtCore.Signal(list)

    def __init__(self, sol, camera,page, parent=None):
        super().__init__(parent)
        self.sol = sol
        self.camera = camera
        self.page = page

    def run(self):
        req = requests.get(f"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol={self.sol}&page={self.page}&api_key=).json()
        photo_lst = []
        self.num = 0
        print(req)
        for i in req['photos']:
            self.num += 1 
            print(1)
            urllib.request.urlretrieve(f"{i['img_src']}",f"photo{self.num}.jpg")
            print(2)
            photo_lst.append(f"photo{self.num}.jpg")
        
 
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

         # Stacking of label
        

        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)
        self.label1 = QLabel()
        self.label2 = QLabel()
        self.stacked_widget.addWidget(self.label1)
        self.stacked_widget.addWidget(self.label2)
        self.button1 = QPushButton("Photos", self)
        self.button1.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.button2 = QPushButton("Email", self)
        self.button2.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        self.box1=QLabel(self.label1)
        self.box1.setGeometry(1100, 100, 800, 900)
        self.box1.setStyleSheet("QLabel{ background-color : rgba(35, 36, 38,89)}")
        

        #button settings
        self.button1.move(150, 30)
        self.button2.move(250, 30)
        self.button1.setFlat(True)
        self.button2.setFlat(True)
        fontbt1 = self.button1.font()
        fontbt1.setPointSize(20)
        fontbt2 = self.button2.font()
        fontbt2.setPointSize(15)

        # set button
        self.button1.setFont(fontbt1)
        self.button2.setFont(fontbt2)

        #click
        self.button1.clicked.connect(self.buttonf1)
        self.button2.clicked.connect(self.buttonf2)
        


    

        #image code 
        self.logo = QLabel(self)
    
        self.SolLabel = QLabel(self.box1)
        self.SolLabel.setText('Earth_date:')
        self.SolLabel.move(100, 100)

        self.Solinput = QLineEdit(self.box1)
        self.Solinput.move(200, 90)
        self.Solinput.resize(280,40)
        self.Solinput.setStyleSheet("background-color: rgba(28, 26, 28,100)")

        self.CameraLabel = QLabel(self.box1)
        
        self.CameraLabel.setText('Camera:')
        self.CameraLabel.move(120,150)

        dropdown = QComboBox(self.box1)
        dropdown.addItems(["FHAZ", "RHAZ", "MAST","CHEMCAM","MAHLI","MARDI","NAVCAM","PANCAM","MINITES"])
        dropdown.move(200, 150)
        dropdown.show()
        self.selected_value = dropdown.currentText()
    
        
        self.PageLabel = QLabel(self.box1)
        self.PageLabel.setText('Page:')
        self.PageLabel.move(140,200)

        self.Pageinput = QLineEdit(self.box1)
        self.Pageinput.setStyleSheet("background-color: rgba(28, 26, 28,100)")
        self.Pageinput.move(200, 190)
        self.Pageinput.resize(280,40)
        
        self.label = QLabel(self)
        self.label.move(300,200)
        self.label.resize(600, 550)
        
        #email page
        box=QLabel(self.label2)
        box.setGeometry(1100, 100, 800, 900)
        box.setStyleSheet("QLabel{ background-color : rgba(35, 36, 38,89)}")





        self.toLabel = QLabel(box)
        self.toLabel.setText('To:')
        self.toLabel.move(50,100)
        self.toinput = QLineEdit(box)
        self.toinput.setFixedSize(600, 40)
        self.toinput.move(100, 100)
        self.toinput.resize(280,40)


        self.subLabel = QLabel(box)
        self.subLabel.setText('Subject:')
        self.subLabel.move(20,200)
        self.subinput = QLineEdit(box)
        self.subinput.setFixedSize(600, 40)
        self.subinput.move(100, 200)
        self.subinput.resize(280,40)


        self.boinput = QLineEdit(box)
        # self.boinput.setFixedSize(600, 550)
        self.boinput.setGeometry(100, 300, 600, 550)
        # self.boinput.move(100, 300)
        # self.boinput.resize(280,40)
       
        send = QPushButton("Send", box)
        send.setStyleSheet("QPushButton { border-radius: 10px;background-color: rgb(4, 108, 110); }")
        send.setFixedSize(90, 40)
        send.move(680,30)
        send.clicked.connect(self.email)





        button = QPushButton("Fetch Image", self.box1)
        font = button.font()
        font.setPointSize(16)
        palette = button.palette()
        palette.setColor(QPalette.ButtonText, Qt.black)
        button.setPalette(palette)
        font.setBold(True)
        button.setFont(font)
        button.setGeometry(500, 400, 200, 60)
        button.setStyleSheet("QPushButton { border-radius: 10px; background-color: rgb(219, 219,72); }")

       
    
    
        fow = QPushButton(">", self)
        fow.setGeometry(1000, 500, 30, 30)
        fow.setStyleSheet("background-color: transparent;")

        fow.clicked.connect(self.foward)

        back = QPushButton("<", self)
        back.setGeometry(10, 500, 30, 30)
        back.setStyleSheet("background-color: transparent;")

        back.clicked.connect(self.back)
        self.num = 100
        self.index = 0
        #logo
        

        pixmap = QPixmap(f"back.png")
        pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo.resize(pixmap.width(), pixmap.height())
        self.logo.move(-50,-10)
        self.logo.setPixmap(pixmap)
        self.logo.show()

        button.clicked.connect(self.Fetch_data)


        #selection
        self.img_list = []
        self.open_image_button = QPushButton("Open Image", box)
        self.open_image_button.move(100, 260)
        self.open_image_button.setStyleSheet("QPushButton{ background-color : blue}")


        self.open_image_button.clicked.connect(self.open_image)

 
   
    def open_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        self.file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "Images (*.png *.xpm *.jpg *.bmp *.gif);;All Files (*)", options=options)
        
        
        
    def email(self):
        for x in self.toinput.text().split(","):
            from_address = "martianchronicles1990@gmail.com"
            to_address = x
            print(self.toinput.text().split(", "))
            password = ""

            message = MIMEMultipart()
            message["Subject"] = "Test Email with Image Attachment from Python"
            message["From"] = from_address
            message["To"] = to_address

            text = MIMEText("This is a test email sent from Python with an image attachment.")
            message.attach(text)
            for i in self.img_list:
                with open(i, "rb") as image:
                    image_data = image.read()
                    self.image_encoded = base64.b64encode(image_data)
                    image = MIMEImage(image_data)
                    message.attach(image)

            server = smtplib.SMTP("smtp.gmail.com", 587) # replace "smtp.example.com" with the hostname of your SMTP server
            server.ehlo()
            server.starttls()
            server.login(from_address, password)
            server.sendmail(from_address, to_address, message.as_string())
            server.quit()
         
        movie = QMovie("sent.gif")
        self.label.setMovie(movie)
        movie.start()  


        

    def buttonf1(self):
            print(1)
            fontbt1 = self.button1.font()
            fontbt1.setPointSize(20)
            self.button1.setFont(fontbt1)

            fontbt2 = self.button1.font()
            fontbt2.setPointSize(15)
            self.button2.setFont(fontbt2)


    def buttonf2(self):
            print(1)
            fontbt2 = self.button1.font()
            fontbt2.setPointSize(20)
            self.button2.setFont(fontbt2)

            fontbt1 = self.button1.font()
            fontbt1.setPointSize(15)
            self.button1.setFont(fontbt1)
            
    def Fetch_data(self):
        input1 = self.Solinput.text()
        input2 = self.selected_value
        input3 = self.Pageinput.text() 
        print(input1,input2,input3)

        self.thread = FetchThread(input1, input2,input3)
        self.thread.start()
        print("number = ", self.num)
        print("pressed")
        self.index += 1
        pixmap = QPixmap(f"photo{self.index}.jpg")
        pixmap = pixmap.scaled(900, 1500, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label.resize(pixmap.width(), pixmap.height())
        self.label.move(60,60)
        self.label.setPixmap(pixmap)
        self.label.show()

    def foward(self):
        if self.index <= self.num-1:
            self.index += 1
            print(self.index)

            pixmap = QPixmap(f"photo{self.index}.jpg")
            pixmap = pixmap.scaled(900, 1500, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label.resize(pixmap.width(), pixmap.height())
            self.label.move(60,100)
            self.label.setPixmap(pixmap)
            self.label.show()
        else:
            self.index = 1
            pixmap = QPixmap(f"photo{self.index}.jpg")
            pixmap = pixmap.scaled(900, 1500, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label.resize(pixmap.width(), pixmap.height())
            self.label.move(60,60)
            self.label.setPixmap(pixmap)
            self.label.show()
    
    def back(self):
        if self.index >= 0:
            self.index -= 1
            print(self.index)
            pixmap = QPixmap(f"photo{self.index}.jpg")
            pixmap = pixmap.scaled(900, 1500, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label.resize(pixmap.width(), pixmap.height())
            self.label.move(60,100)
            self.label.setPixmap(pixmap)
            self.label.show()
        else:
            self.index = self.num 
            print(self.index)
            pixmap = QPixmap(f"photo{self.index}.jpg")
            pixmap = pixmap.scaled(900, 1500, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label.resize(pixmap.width(), pixmap.height())
            self.label.move(60,60)
            self.label.setPixmap(pixmap)
            self.label.show()



App = QApplication(sys.argv)
window = Window()

window.setStyleSheet("QMainWindow {background-image: url(background.png);}")

indx = 0

sys.exit(App.exec())
# window.setStyleSheet("QMainWindow {background-image: url(background.png);}")