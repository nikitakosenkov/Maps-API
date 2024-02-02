import sys
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
import requests


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('04.ui', self)
        self.map_zoom = 10
        delta = 0.2
        self.map_l = 'map'
        self.map_ll = [37.620431, 55.753789]
        self.press_delta = 12.5 / (self.map_zoom ** 3)
        self.render_map()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_PageUp and self.map_zoom < 17:
            self.map_zoom += 1
            self.press_delta = 12.5 / (self.map_zoom ** 3)
        if key == Qt.Key_PageDown and self.map_zoom > 0:
            self.map_zoom -= 1
            if self.map_zoom > 0:
                self.press_delta = 12.5 / (self.map_zoom ** 3)
            else:
                self.press_delta = 12.5
            print(self.press_delta)
        if key == Qt.Key_Left:
            self.map_ll[0] -= self.press_delta * self.map_zoom
        if key == Qt.Key_Right:
            self.map_ll[0] += self.press_delta * self.map_zoom
        if key == Qt.Key_Up:
            self.map_ll[1] += self.press_delta * self.map_zoom
        if key == Qt.Key_Down:
            self.map_ll[1] -= self.press_delta * self.map_zoom
        if key == Qt.Key_G:
            self.map_l = 'sat,skl'
        if key == Qt.Key_S:
            self.map_l = 'sat'
        if key == Qt.Key_M:
            self.map_l = 'map'

        self.render_map()

    def render_map(self):
        params = {
            "ll": f'{self.map_ll[0]},{self.map_ll[1]}',
            "l": self.map_l,
            'z': self.map_zoom

        }
        resspons = requests.get('https://static-maps.yandex.ru/1.x/', params=params)
        with open('tmp.png', 'wb') as tmp:
            tmp.write(resspons.content)

        pixmap = QPixmap()
        pixmap.load('tmp.png')

        self.label.setPixmap(pixmap)


app = QApplication(sys.argv)
ex = MainWindow()
ex.show()
sys.exit(app.exec_())
