from PyQt6.QtCore import QFileInfo
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog
from PyQt6.QtWidgets import QFileDialog


class File(object):
    def __init__(self, window_f, text_widget, inits):
        super().__init__()

        self.inits = inits

        self.supported_types = ['txt', 'html']

        self.window = window_f
        self.text_widget = text_widget
        window_f.file_menu = window_f.menuBar().addMenu("File")

        # Add option to save the file
        window_f.save_file = QAction(QIcon("icons/diskette.png"), 'Save File', window_f)
        window_f.save_file.setShortcut("Ctrl+S")
        window_f.save_file.triggered.connect(self.save)
        window_f.file_menu.addAction(window_f.save_file)

        # Add option to open a file
        window_f.open_file = QAction('Open File', window_f)
        window_f.open_file.setIcon(QIcon('icons/document.png'))
        window_f.open_file.setShortcut("Ctrl+O")
        window_f.open_file.triggered.connect(self.open)
        window_f.file_menu.addAction(window_f.open_file)

        # Add option to open a new window
        window_f.new_box = QAction('New Window', window_f)
        window_f.new_box.setShortcut("Ctrl+N")
        window_f.new_box.triggered.connect(self.new_box)
        window_f.file_menu.addAction(window_f.new_box)

        # Add option to print a file
        window_f.print_file = QAction(QIcon("print.png"), 'Print', window_f)
        window_f.print_file.setIcon(QIcon('icons/printer.png'))
        window_f.print_file.setShortcut("Ctrl+P")
        window_f.print_file.triggered.connect(self.print)
        window_f.file_menu.addAction(window_f.print_file)

        # Add option for print preview
        window_f.print_preview = QAction(QIcon("printprev.png"), 'Print Preview', window_f)
        window_f.print_preview.triggered.connect(self.preview)
        window_f.file_menu.addAction(window_f.print_preview)

        # Add option to export to pdf
        window_f.exportPDF = QAction(QIcon("pdf.png"), 'PDF Export', window_f)
        window_f.exportPDF.setIcon(QIcon('icons/export.png'))
        window_f.exportPDF.triggered.connect(self.export_pdf)
        window_f.file_menu.addAction(window_f.exportPDF)

    def new_box(self):
        self.window_f = self.inits.make_main_window()
        self.window_f.show()
        return self.window_f

    def save(self):
        buffer = self.text_widget.toHtml()
        if buffer:
            file_dialog = QFileDialog(self.window)
            # convert list of supported types to a string that conforms to the search format
            supported_types_string = '*.' + ';;*.'.join(self.supported_types)
            file_name = file_dialog.getSaveFileName(self.window, 'Save File', '', supported_types_string)
            if file_name != ('', ''):
                f = open(file_name[0], 'w')
                if f.closed:
                    return
                f.write(buffer)
                f.close()

    def open(self, file_name=None):
        # I don't really understand why file_name would be False
        # instead of none, but apparently that's how it is
        if file_name is False:
            file_dialog = QFileDialog(self.window)
            # convert list of supported types to a string that conforms to the search format
            supported_types_string = '*.' + ';;*.'.join(self.supported_types)
            file_name, _ = file_dialog.getOpenFileName(self.window, 'Open File', supported_types_string)

        if file_name:
            try:
                file = open(file_name, 'r')
            except:
                return False

            if file.closed:
                return
            self.editor()
            with file:
                text = file.read()
                self.text_widget.setText(text)

        return True

    def editor(self):
        self.text_widget = self.inits.make_text_widget(self.window)
        self.window.setCentralWidget(self.text_widget)

    def print(self):
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        print_dialog = QPrintDialog(printer)
        if print_dialog.exec():
            self.text_widget.document().print(print_dialog.printer())

    def preview(self):
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        file_dialog = QPrintPreviewDialog(printer)
        file_dialog.paintRequested.connect(self.paint_preview)
        file_dialog.exec()

    def paint_preview(self, printer):
        self.text_widget.document().print(printer)

    def export_pdf(self):
        fn, _ = QFileDialog.getSaveFileName(self.text_widget, "Export PDF", None, "PDF Files (.pdf);;All Files()")

        if fn != '':
            if QFileInfo(fn).suffix() == "":
                fn += '.pdf'
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setOutputFileName(fn)
            print(self.text_widget.toHtml)
            print(printer)
            self.text_widget.document().print(printer)
