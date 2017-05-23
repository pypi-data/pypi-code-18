from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Widget(QWidget):

    def __init__(self):
        super(Widget, self).__init__()
        button = QPushButton("Open")
        layout = QHBoxLayout(self)
        layout.addWidget(button)
        button.clicked.connect(self.click)

    def click(self):
        files = QFileDialog.getOpenFileNames(
            self,
            "Choose",
            "",
            self.tr("tseries (*.py)"),
            None,
            QFileDialog.DontUseNativeDialog)
        print(files)


def main():
    import sys
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
