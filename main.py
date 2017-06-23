import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit
from PyQt5 import QtGui, QtCore, QtWidgets


class MyLabel(QLabel):

    def __init__(self, text_str, window, posx, posy):
        super().__init__(text_str, window)
        self.move(posx, posy)
        self.setFixedWidth(250)


class MyEntry(QLineEdit):

    def __init__(self, window, posx, posy, init_val):
        super().__init__(window)

        rx = QtCore.QRegExp('^[1-9]\d{2}$')
        validator = QtGui.QRegExpValidator(rx)
        self.setValidator(validator)
        self.move(posx, posy)
        self.setText(str(init_val))



class Window(QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 500, 600)
        self.setFixedSize(500, 600)
        self.setWindowTitle("Smart Security Preventivi")
        self.setWindowIcon(QtGui.QIcon('logo.jpg'))

        extractAction = QtWidgets.QAction("Exit", self)
        extractAction.setShortcut("Ctrl+Q")
        extractAction.setStatusTip("Leave the App")
        extractAction.triggered.connect(self.close_application)

        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("&File")
        fileMenu.addAction(extractAction)

        self.home()

    def home(self):

        # btn = QPushButton("Calcola", self)
        # btn.setToolTip('Calcola il preventivo')
        # btn.resize(btn.sizeHint())
        # btn.move(50, 50)

        lbl1 = MyLabel('Porte d\' Ingresso', self, 50, 50)
        lbl2 = MyLabel('Finestre / Porte Finestre', self, 50, 100)
        lbl3 = MyLabel('Disimpegni dell\' abitazione', self, 50, 150)

        self.lblSum = QtWidgets.QLabel('', self)
        self.lblSum.move(350, 200)

        self.entry1Edit = MyEntry(self, 350, 50, 1)
        self.entry1Edit.textChanged[str].connect(self.onChanged)
        self.entry2Edit = MyEntry(self, 350, 100, 0)
        self.entry2Edit.textChanged[str].connect(self.onChanged)
        self.entry3Edit = MyEntry(self, 350, 150, 0)
        self.entry3Edit.textChanged[str].connect(self.onChanged)

        self.show()

    def close_application(self):
        # Si potrebbe mettere un pop up sei sicuro di uscire
        sys.exit()

    def onChanged(self, text):

        costante = 1100.0
        porte_ingresso = 50.0
        finestre = 50.0
        disimpegni = 74.0
        sensore_movimento = 74.0
        telecomandi = 51.0
        terrazzi = 215.0
        rivelatore_allagamento = 74.0
        rivelatore_fumo = 108.0
        rivelatore_monossido = 174.0

        if self.entry1Edit.text() == '':
            nbr1 = 0
        else:
            nbr1 = int(self.entry1Edit.text())

        if self.entry2Edit.text() == '':
            nbr2 = 0
        else:
            nbr2 = int(self.entry2Edit.text())

        if self.entry3Edit.text() == '':
            nbr3 = 0
        else:
            nbr3 = int(self.entry3Edit.text())

        sum = nbr1 * 120 + nbr2 * 80 + nbr3 * 20
        self.lblSum.setText(str(sum))
        self.lblSum.adjustSize()


def run():
    app = QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

run()