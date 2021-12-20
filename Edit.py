
from PyQt6.QtGui import QIcon, QAction


class Edit(object):
    def __init__(self, window_e, text_widget):
        super().__init__()

        self.window = window_e
        self.text_widget = text_widget
        # create the insert toolbar menu
        self.window.file_menu = self.window.menuBar().addMenu('Edit')

        # add options to the new menu buttons
        self.window.undoAction = QAction(QIcon('icons/undo.png'), "Undo", self.window)
        self.window.undoAction.setShortcut("Ctrl+Z")
        self.window.undoAction.triggered.connect(text_widget.undo)
        self.window.file_menu.addAction(self.window.undoAction)

        self.window.redoAction = QAction(QIcon('icons/redo.png'), "Redo", self.window)
        self.window.redoAction.setShortcut("Ctrl+Y")
        self.window.redoAction.triggered.connect(text_widget.redo)
        self.window.file_menu.addAction(self.window.redoAction)

        self.window.cutAction = QAction(QIcon('icons/scissors.png'), "Cut", self.window)
        self.window.cutAction.setShortcut("Ctrl+X")
        self.window.cutAction.triggered.connect(text_widget.cut)
        self.window.file_menu.addAction(self.window.cutAction)

        self.window.copyAction = QAction(QIcon('icons/copy.png'), "Copy", self.window)
        self.window.copyAction.setShortcut("Ctrl+C")
        self.window.cutAction.triggered.connect(text_widget.copy)
        self.window.file_menu.addAction(self.window.copyAction)

        self.window.pasteAction = QAction(QIcon('icons/paste.png'), "Paste", self.window)
        self.window.pasteAction.setShortcut("Ctrl+V")
        self.window.pasteAction.triggered.connect(text_widget.paste)
        self.window.file_menu.addAction(self.window.pasteAction)
