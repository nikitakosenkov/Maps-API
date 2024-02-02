import sys

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
import requests


spn = int(input('Введите масштаб '))
coords = [float(i) for i in input('Введите координаты через пробел ').split()]


class MainWindow(QMainWindow):
    g_map: QLabel

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('ui_class_work.ui', self)

        global spn, coords
        # 5
        # 37.977751 55.757718
        self.map_zoom = spn + 1
        self.map_ll = coords
        self.map_l = 'map'
        self.press_delta = 12.5 / (self.map_zoom ** 3)

        self.render_map()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_PageUp and self.map_zoom < 17:
            self.map_zoom += 1
            self.press_delta = 12.5 / (self.map_zoom ** 3)
            print(self.press_delta)
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

        self.render_map()

    def render_map(self):
        map_params = {
            "ll": f'{self.map_ll[0]},{self.map_ll[1]}',
            "l": self.map_l,
            'z': self.map_zoom,
        }
        response = requests.get('https://static-maps.yandex.ru/1.x/',
                                params=map_params)
        with open('tmp.png', mode='wb') as tmp:
            tmp.write(response.content)

        pixmap = QPixmap()
        pixmap.load('tmp.png')

        self.g_map.setPixmap(pixmap)


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())
