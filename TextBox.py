"""
    TextBox.py
"""

import re
import sys
import ctypes

from os.path import exists

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTextBrowser, QMenu, QDialog

from Edit import *
from File import *
from InsertMenu import *
from TextStyle import *


# Main window. Instantiates with a text box
class MainWindow(QMainWindow, QApplication):
    def __init__(self):
        super().__init__()

        # Temporary title
        self.setWindowTitle("Happy Little Notes")
        self.setWindowIcon(QIcon('icons/tree.png'))
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('icons/tree.png')

        # create a text widget
        text_box = TextWidget(self)

        # add file menu to toolbar
        inits = InitFunctions()
        self.file = File(self, text_box, inits)

        Zoom(self, text_box)

        # add style menu to toolbar
        self.style = Style(self)

        # add insert menu to toolbar
        self.insert = Insert(self)

        # add edit menu to toolbar
        self.edit = Edit(self, text_box)

        # adds created layout to central widget
        self.setCentralWidget(text_box)

        # popup window that can be defined by other functions as needed
        self.w = None

        # adds files section to toolbar
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)


# Text box with text browser and text edit interaction capabilities
# Member function for inserting hyperlinks into the text
class TextWidget(QTextBrowser):
    def __init__(self, window_t):
        super().__init__()

        self.window = window_t
        self.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextEditorInteraction | Qt.TextInteractionFlag.LinksAccessibleByMouse)
        self.setOpenExternalLinks(True)

        self.setUndoRedoEnabled(True)

        # this is enacted when a link that is not external is clicked
        self.anchorClicked.connect(self.on_anchor_clicked)

    # triggered when the text box is right clicked
    def contextMenuEvent(self, event):
        # create a menu at click location with the default right click options
        self.window.menu = self.createStandardContextMenu(event.pos())

        # add hyperlink option to menu
        self.window.hyperlink = QAction('Insert Hyperlink', self.window)
        self.window.hyperlink.setIcon(QIcon('icons/hyperlink.png'))
        self.window.hyperlink.triggered.connect(self.window.insert.display_hyperlink_popup)
        self.window.menu.addAction(self.window.hyperlink)

        self.window.note_link = QAction('Link to Another Note', self.window)
        self.window.note_link.triggered.connect(self.window.insert.display_note_link_popup)
        self.window.menu.addAction(self.window.note_link)

        # display menu
        self.window.menu.popup(event.globalPos())

    def insert_hyperlink(self, text, url):
        # if given link does not start with https://
        # add it to the beginning of the string
        if re.match("https://", url) is None:
            url = "https://" + url
        # insert hyperlink
        self.insertHtml("<a href = " + url + ">" + text + "</a>")
        self.insertHtml("<p style=\"color:black;\">&nbsp;</p>")

    def insert_note_link(self, text, destination):
        # if given link does not have a valid file type,
        # add one to the end of the string

        supported = False
        for typename in self.window.file.supported_types:
            if re.match('.*\.' + typename + '$', destination):
                supported = True
                break
        # if the name doesn't end in a supported type, add one that
        # corresponds to an existing file if possible, prioritizing supported types list order
        if supported is False:
            for typename in self.window.file.supported_types:
                temp = destination + "." + typename
                if exists(temp):
                    destination = temp
                    break

        # insert link
        self.insertHtml("<a href = " + destination + ">" + text + "</a>")
        self.insertHtml("<p style=\"color:black;\">&nbsp;</p>")

    # this function is called when a non-external link is clicked
    def on_anchor_clicked(self, url):
        # clicking the link automatically opens the file
        # in the current window. I couldn't figure out how
        # to prevent that without breaking the external link
        # capability, so instead I saved the text to a variable
        # and put it back in after opening the link in a new window.
        # This seems to work, but I am suspicious of it
        text = self.toHtml()

        # open a new window, and open the file in it
        file_name = str(url.toString())
        new_window = self.window.file.new_box()
        if new_window.file.open(file_name) is False:
            error_label = QLabel("Error: file " + file_name + " does not exist")
            new_window.setCentralWidget(error_label)

        self.setText(text)


# Init functions that can be referenced if an init_functions object is passed to
# another file where TextBox is not imported.
# Needed since File.py cannot import TextBox
class InitFunctions(object):
    def make_main_window(self):
        return MainWindow()

    def make_text_widget(self, mwindow):
        return TextWidget(mwindow)


class Zoom(object):
    def __init__(self, window_1, text_box):
        super().__init__()

        self.zoom_level = 0
        self.win = window_1

        # self.text_widget = text_box
        self.text_widget = text_box

        # Create View Menu for Zoom Option
        window_1.file_menu = window_1.menuBar().addMenu('View')
        window_1.zoom_menu = QMenu('Zoom', window_1)
        window_1.zoom_menu.setIcon(QIcon('icons/zoom.png'))

        window_1.zoom_num = QAction('Zoom Level', window_1)
        window_1.zoom_num.triggered.connect(self.show_zoom)
        window_1.zoom_in = QAction('Zoom in', window_1)
        window_1.zoom_in.setIcon(QIcon('icons/zoom_in.png'))
        window_1.zoom_in.setShortcut("Ctrl++")
        window_1.zoom_in.triggered.connect(self.zoom_inward)
        window_1.zoom_out = QAction('Zoom out', window_1)
        window_1.zoom_out.setIcon(QIcon('icons/zoom_out.png'))
        window_1.zoom_out.setShortcut("Ctrl+-")
        window_1.zoom_out.triggered.connect(self.zoom_outward)

        window_1.zoom_menu.addAction(window_1.zoom_num)
        window_1.zoom_menu.addAction(window_1.zoom_in)
        window_1.zoom_menu.addAction(window_1.zoom_out)
        window_1.file_menu.addMenu(window_1.zoom_menu)

    def zoom_inward(self):
        self.zoom_level += 1
        self.text_widget.zoomIn(self.zoom_level)

    def zoom_outward(self):
        self.zoom_level -= 1
        self.text_widget.zoomOut(self.zoom_level)

    def show_zoom(self):
        self.pop = Popup(self.zoom_level, self.win)
        self.pop.show()


class Popup(QDialog):
    def __init__(self, name, parent):
        super().__init__(parent)
        self.resize(600, 300)
        self.label = QLabel(name, parent.win)


app = QApplication(sys.argv)

window = MainWindow()

window.show()

sys.exit(app.exec())
