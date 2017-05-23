from qtpy import uic
from qtpy.QtWidgets import QDialog, QApplication

# about_ui, _ = uic.loadUiType('about.ui')


# class TSAboutDialog(QDialog, about_ui):
#     def __init__(self):
#         super(TSAboutDialog, self).__init__()
#         self.setupUi(self)
#         self.setWindowTitle("TSAnalyzer - About")

class TSAboutDialog(QDialog):
    def __init__(self):
        super(TSAboutDialog, self).__init__()
        # self.setupUi(self)
        uic.loadUi('about.ui', self)
        self.setWindowTitle("TSAnalyzer - About")


def main():
    import sys
    app = QApplication(sys.argv)
    windows = TSAboutDialog()
    windows.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
