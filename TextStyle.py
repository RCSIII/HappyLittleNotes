import qdarktheme
from PyQt6 import QtWidgets
from PyQt6.QtGui import QColor, QAction, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow


class Style(QMainWindow, QApplication):
    def __init__(self, window_s):
        super().__init__()

        # create the style toolbar button
        self.window = window_s
        window_s.file_menu = window_s.menuBar().addMenu("Style")

        # add font option to the new menu button
        window_s.font_change = QAction('Change Font', window_s)
        window_s.font_change.setIcon(QIcon('icons/text-font.png'))
        window_s.font_change.triggered.connect(self.font_choice)
        window_s.file_menu.addAction(window_s.font_change)

        # add color picker option to the new menu button
        window_s.color_change = QAction('Change Color', window_s)
        window_s.color_change.setIcon(QIcon('icons/color-circle.png'))
        window_s.color_change.triggered.connect(self.color_choice)
        window_s.file_menu.addAction(window_s.color_change)

        # add dark theme option
        window_s.dark_theme = QAction('Dark Theme', window_s)
        window_s.dark_theme.triggered.connect(self.dark_theme)
        window_s.file_menu.addAction(window_s.dark_theme)

        # add light theme option to the style section
        window_s.light_theme = QAction('Light Theme', window_s)
        window_s.light_theme.triggered.connect(self.light_theme)
        window_s.file_menu.addAction(window_s.light_theme)

        # add highlight text option ot the style section
        window_s.highlight_text = QAction('Highlight', window_s)
        window_s.highlight_text.setIcon(QIcon('icons/highlighter.png'))
        window_s.highlight_text.triggered.connect(self.highlight)
        window_s.file_menu.addAction(window_s.highlight_text)

        # set light theme on initialization
        self.light_theme()

    def font_choice(self):
        f, valid = QtWidgets.QFontDialog.getFont()
        if valid:
            self.window.centralWidget().setCurrentFont(f)

    def color_choice(self):
        color = QtWidgets.QColorDialog.getColor()
        self.window.centralWidget().setTextColor(color)

    def highlight(self):
        white = QColor('white')
        yellow = QColor('yellow')
        random = QColor(QColor(0, 0, 0, 255))
        if self.window.centralWidget().textBackgroundColor().getRgb() == white.getRgb() or self.window.centralWidget().textBackgroundColor().getRgb() == random.getRgb():
            self.window.centralWidget().setTextBackgroundColor(yellow)
        elif self.window.centralWidget().textBackgroundColor().getRgb() == yellow.getRgb():
            self.window.centralWidget().setTextBackgroundColor(white)

    def dark_theme(self):
        self.window.setStyleSheet(qdarktheme.load_stylesheet())

    def light_theme(self):
        self.window.setStyleSheet(qdarktheme.load_stylesheet("light"))