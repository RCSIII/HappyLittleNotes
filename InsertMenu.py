"""
InsertMenu.py
"""

from PyQt6.QtCore import QRect
from PyQt6.QtGui import QAction, QPixmap, QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton


class Insert(object):
    def __init__(self, window_i):
        super().__init__()

        self.window = window_i

        # create the insert toolbar menu
        self.window.file_menu = self.window.menuBar().addMenu('Insert')

        # add options to the menu
        self.window.hyperlink = QAction('Hyperlink', self.window)
        self.window.hyperlink.setIcon(QIcon('icons/hyperlink.png'))
        self.window.hyperlink.triggered.connect(self.display_hyperlink_popup)
        self.window.file_menu.addAction(self.window.hyperlink)

        self.window.note_link = QAction('Link to Another Note', self.window)
        self.window.note_link.triggered.connect(self.display_note_link_popup)
        self.window.file_menu.addAction(self.window.note_link)

        self.window.bulletlist = QAction('Bulleted List', self.window)
        self.window.bulletlist.setIcon(QIcon('icons/menu.png'))
        self.window.bulletlist.triggered.connect(self.insert_bullet_list)
        self.window.file_menu.addAction(self.window.bulletlist)

        self.window.numberlist = QAction('Numbered List', self.window)
        self.window.numberlist.setIcon(QIcon('icons/list.png'))
        self.window.numberlist.triggered.connect(self.insert_number_list)
        self.window.file_menu.addAction(self.window.numberlist)

        window_i.image = QAction('Display Image', window_i)
        window_i.image.setIcon(QIcon('icons/image.png'))
        window_i.image.triggered.connect(self.display_image)
        window_i.file_menu.addAction(window_i.image)

    def display_hyperlink_popup(self):
        self.window.w = HyperlinkPopup(self.window)
        self.window.w.show()

    def display_note_link_popup(self):
        self.window.w = NoteLinkPopup(self.window)
        self.window.w.show()

    def insert_bullet_list(self):
        self.window.centralWidget().insertHtml("<ul><li>&nbsp;</li></ul>")

    def insert_number_list(self):
        self.window.centralWidget().insertHtml("<ol><li>&nbsp;</li></ol>")

    def display_image(self):
        self.window.w = ImageGrab()
        self.window.w.setWindowTitle("Happy Little Notes")
        self.window.w.show()


class HyperlinkPopup(QWidget):
    def __init__(self, window):
        QWidget.__init__(self)

        self.window = window

        # create layout
        layout = QVBoxLayout()
        self.setGeometry(QRect(300, 100, 300, 100))

        # create text boxes
        self.hyperlink_text = QLineEdit()
        self.hyperlink_URL = QLineEdit()

        # add text boxes to layout
        layout.addWidget(QLabel("hyperlink text:"))
        layout.addWidget(self.hyperlink_text)
        layout.addWidget(QLabel("hyperlink URL:"))
        layout.addWidget(self.hyperlink_URL)

        # create button and add it to layout
        button_insert_hyperlink = QPushButton()
        button_insert_hyperlink.setText("Insert Hyperlink")
        layout.addWidget(button_insert_hyperlink)

        # set a function to be enacted when button is clicked
        button_insert_hyperlink.clicked.connect(self.button_insert_hyperlink_clicked)

        self.setLayout(layout)

    def button_insert_hyperlink_clicked(self):
        # get info from text boxes and pass to insert_link function
        text = self.hyperlink_text.text()
        url = self.hyperlink_URL.text()
        self.window.centralWidget().insert_hyperlink(text, url)
        self.close()

class NoteLinkPopup(QWidget):
    def __init__(self, window):
        QWidget.__init__(self)

        self.window = window

        # create layout
        layout = QVBoxLayout()
        self.setGeometry(QRect(300, 100, 300, 100))

        # create text boxes
        self.link_text = QLineEdit()
        self.link_destination = QLineEdit()

        # add text boxes to layout
        layout.addWidget(QLabel("link text:"))
        layout.addWidget(self.link_text)
        layout.addWidget(QLabel("name of note to be linked:"))
        layout.addWidget(self.link_destination)

        # create button and add it to layout
        button_insert_link = QPushButton()
        button_insert_link.setText("Insert link")
        layout.addWidget(button_insert_link)

        # set a function to be enacted when button is clicked
        button_insert_link.clicked.connect(self.button_insert_link_clicked)

        self.setLayout(layout)

    def button_insert_link_clicked(self):
        # get info from text boxes and pass to insert_hyperlink function
        text = self.link_text.text()
        url = self.link_destination.text()
        self.window.centralWidget().insert_note_link(text, url)
        self.close()
        

class ImageLabel(QLabel):
    def __init__(self):
        super().__init__()

        self.setText('\n\n Drop Image Here \n\n')
        self.setStyleSheet('''
            QLabel[
                border: 4px dashed #aaa
            ]
        ''')

        def setPixMap(self, image):
            super().setPixmap(image)


class ImageGrab(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)

        layout = QVBoxLayout()

        self.photoViewer = ImageLabel()
        layout.addWidget(self.photoViewer)

        self.setLayout(layout)

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            # event.setDropAction(Qt.CopyAction)
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.set_image(file_path)
            event.accept()

        else:
            event.ignore()

    def set_image(self, file_path):
        self.photoViewer.setPixmap(QPixmap(file_path))
