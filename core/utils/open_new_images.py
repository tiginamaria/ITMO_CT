# This file helps to get new photos location on the computer

'''
***** Example of typical usage *****
Create new object with type PhotoSelector:
selected_photos = PhotoSelector(sys.argv)
Create variable where list of new photo paths will be stored:
selected_photos_path = selected_photos.run_UI()
Delete object in order to free up memory after usage:
del(selected_photo)
'''

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog

class PhotoSelector(QApplication):
    
    def __init__(self, argv):
        super().__init__(argv)
        self.screen_width = self._get_window_width()
        self.screen_height = self._get_window_height()
        self.dialog_window = DialogWidget(self.screen_width, self.screen_height)
        
    def run_UI(self):
        response = self.dialog_window.open_file_names_dialog()
        return response
    
    def _get_window_width(self):
        return self.primaryScreen().size().width()
    
    def _get_window_height(self):
        return self.primaryScreen().size().height()

class DialogWidget(QWidget):

    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.window_width = 640
        self.window_height = 480
        self.title = 'Select photos to upload'
        self.left = (self.screen_width - self.window_width) / 2
        self.top = (self.screen_height - self.window_height) / 2

    def open_file_names_dialog(self):
        self.setGeometry(self.left, self.top, self.window_width, self.window_height)
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, self.title, "","All files (*);; All Image Files (*.jpg *.jpeg *.png)", options=options)
        return files
