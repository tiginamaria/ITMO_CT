# This file asks user about his/her current location in latitude/longitude form or in address form

'''
***** Example of typical usage *****
Create new object with type UserLocation:
user_location_ui = UserLocation()
Create variable where will be stored user's GPS location or user's address
user_location_list = user_location_ui.run_UI()
How to understand what is inserted?
* List contains 1 element - address inserted
* List contains 2 elements - GPS inserted
'''

import sys
from PyQt5.QtCore import * 
from PyQt5.QtGui import *
from PyQt5.QtWidgets import * 

class UserLocation(QApplication):
    
    def __init__(self):
        
        super().__init__([])
        self.screen_width = self._get_window_width()
        self.screen_height = self._get_window_height()
        self._setup_UI()
        
    def _setup_UI(self):
        
        self.window = QWidget()
        self.window_width = 600
        self.window_height = 300
        self.left = (self.screen_width - self.window_width) / 2
        self.top = (self.screen_height - self.window_height) / 2
        self.window.setGeometry(self.left, self.top, self.window_width, self.window_height)
    
    def run_UI(self):
        
        self._select_input_type()
        self.window.show()
        self.exec_()
        return self.response

    def _select_input_type(self):
        
        general_layout = QVBoxLayout()
        
        label_1 = QLabel('Input your location by latitude and longitude')
        label_1.setAlignment(Qt.AlignCenter)
        label_1.setFont(QFont('Times', 16))
        general_layout.addWidget(label_1)
        
        layout_latlong = QHBoxLayout()
        
        label_lat = QLabel('Latitude')
        label_lat.setFont(QFont('Times', 16))
        layout_latlong.addWidget(label_lat)
        
        input_lat = QLineEdit()
        input_lat.setFont(QFont('Times', 16))
        layout_latlong.addWidget(input_lat)
        
        label_long = QLabel('Longitude')
        label_long.setFont(QFont('Times', 16))
        layout_latlong.addWidget(label_long)
        
        input_long = QLineEdit()
        input_long.setFont(QFont('Times', 16))
        layout_latlong.addWidget(input_long)
        
        general_layout.addLayout(layout_latlong)
        
        button_1 = QPushButton('Confirm')
        button_1.setFont(QFont('Times', 16))
        button_1.clicked.connect(lambda: self.return_response([input_lat.text(), input_long.text()]))
        general_layout.addWidget(button_1)
        
        label_2 = QLabel('Input your location by address')
        label_2.setAlignment(Qt.AlignCenter)
        label_2.setFont(QFont('Times', 16))
        general_layout.addWidget(label_2)
        
        input_address = QLineEdit()
        input_address.setFont(QFont('Times', 16))
        general_layout.addWidget(input_address)
        
        button_2 = QPushButton('Confirm')
        button_2.setFont(QFont('Times', 16))
        button_2.clicked.connect(lambda: self.return_response([input_address.text()]))
        general_layout.addWidget(button_2)
        
        self.window.setLayout(general_layout)

    def return_response(self, response):
        self.response = response
        self.window.close()
        return
        
    def _get_window_width(self):
        return self.primaryScreen().size().width()

    def _get_window_height(self):
        return self.primaryScreen().size().height()
