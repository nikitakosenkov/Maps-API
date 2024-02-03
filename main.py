import sys
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
import requests
from pprint import pprint


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('04.ui', self)
        self.map_zoom = 10
        delta = 0.2
        self.map_l = 'map'
        self.postal_code = ''
        self.post_flag = False
        self.lineEdit.setEnabled(False)
        self.pushButton_2.clicked.connect(self.onoff)
        self.pushButton.clicked.connect(self.find_obj)
        self.pushButton_3.clicked.connect(self.reset)
        self.pushButton_4.clicked.connect(self.post)
        self.map_ll = [37.620431, 55.753789]
        self.press_delta = 12.5 / (self.map_zoom ** 3)
        self.pts = []
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
            'z': self.map_zoom,
            "pt": '~'.join(self.pts)

        }
        resspons = requests.get('https://static-maps.yandex.ru/1.x/', params=params)
        with open('tmp.png', 'wb') as tmp:
            tmp.write(resspons.content)

        pixmap = QPixmap()
        pixmap.load('tmp.png')

        self.label.setPixmap(pixmap)

    def onoff(self):
        if self.pushButton_2.text() == 'off':
            self.lineEdit.setEnabled(True)
            self.pushButton_2.setText('on')
        else:
            self.lineEdit.setEnabled(False)
            self.pushButton_2.setText('off')

    def find_obj(self):
        self.label_13.clear()
        self.postal_code = ''
        self.post_flag = False
        toponym_to_find = self.lineEdit.text()
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": toponym_to_find,
            "format": "json"}

        response = requests.get(geocoder_api_server, params=geocoder_params)
        if not response:
            pass
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"]
        full_adress = toponym['metaDataProperty']['GeocoderMetaData']['text']
        try:
            self.postal_code = toponym['metaDataProperty']['GeocoderMetaData']['Address']['postal_code']
        except Exception:
            self.postal_code = 'У введеного адреса нету почтового индекса'
        self.label_12.setText(full_adress)
        toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
        self.map_ll = [float(toponym_longitude), float(toponym_lattitude)]
        self.pts.append(toponym_longitude + ',' + toponym_lattitude)
        self.render_map()

    def reset(self):
        try:
            self.pts.pop()
        except Exception:
            pass
        self.label_12.clear()
        self.label_13.clear()
        self.postal_code = ''
        self.post_flag = False
        self.render_map()

    def post(self):
        if self.post_flag is False and self.postal_code != '':
            self.label_13.setText(self.postal_code)
            self.post_flag = True
        elif self.post_flag is True:
            self.post_flag = False
            self.label_13.clear()


app = QApplication(sys.argv)
ex = MainWindow()
ex.show()
sys.exit(app.exec_())
