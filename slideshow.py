from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QMovie

app = QApplication([])
label = QLabel()
movie = QMovie("sent.gif")
label.setMovie(movie)
label.show()
movie.start()
app.exec_()
