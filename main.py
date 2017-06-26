import sys
import time
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QRadioButton
from PyQt5 import QtGui, QtCore, QtWidgets

from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from django.http import HttpResponse

class MyLabel(QLabel):

    def __init__(self, text_str, window, posx, posy):
        super().__init__(text_str, window)
        self.move(posx, posy)
        self.setFixedWidth(310)


class MyEntry(QLineEdit):

    def __init__(self, window, posx, posy, init_val, min_val=0, max_val=30):
        super().__init__(window)

        self.min_val = min_val
        self.max_val = max_val
        rx = QtCore.QRegExp('^[0-9]\d{2}$')
        validator = QtGui.QRegExpValidator(rx)
        self.setValidator(validator)
        self.move(posx, posy)
        self.setText(str(init_val))
        self.textChanged[str].connect(self.validate_min_max)

    def validate_min_max(self):

        entry_txt = 0
        if self.text() != '':
            entry_txt = int(self.text())
        if entry_txt > self.max_val:
            self.setText(str(self.max_val))
        if entry_txt < self.min_val:
            self.setText(str(self.min_val))


class RadioButtonPair(QtWidgets.QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)
        self.button_group = QtWidgets.QButtonGroup(self)

        self.b1 = QRadioButton("No")
        self.b1.setChecked(True)
        self.button_group.addButton(self.b1)
        layout.addWidget(self.b1)

        self.b2 = QRadioButton("Si")
        self.button_group.addButton(self.b2)
        layout.addWidget(self.b2)

        w = self.sizeHint().width()
        h = self.sizeHint().height()
        self.setFixedSize(w, h)


class Window(QMainWindow):

    def __init__(self):
        super(Window, self).__init__()

        self.removePdfs()
        self.maxSensorNbr = 30

        x_win_dim = 550
        y_win_dim = 800
        self.setGeometry(100, 100, x_win_dim, y_win_dim)
        self.setFixedSize(x_win_dim, y_win_dim)
        self.setWindowTitle("Smart Security Preventivi")
        self.setWindowIcon(QtGui.QIcon('logo.jpg'))

        newAction = QtWidgets.QAction("Nuovo...", self)
        newAction.setShortcut("Ctrl+N")
        newAction.setStatusTip("Nuovo Preventivo")
        newAction.triggered.connect(self.new_application)

        exportAction = QtWidgets.QAction("Export PDF", self)
        exportAction.setStatusTip("Esporta PDF")
        exportAction.triggered.connect(self.exportPDF_application)

        extractAction = QtWidgets.QAction("Exit", self)
        extractAction.setShortcut("Ctrl+Q")
        extractAction.setStatusTip("Chiudi App")
        extractAction.triggered.connect(self.close_application)

        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("&File")
        fileMenu.addAction(newAction)
        fileMenu.addAction(exportAction)
        fileMenu.addAction(extractAction)

        self.home()

    def home(self):

        x_label = 40
        x_entry = 400

        lbl1 = MyLabel('Porte d\' Ingresso', self, x_label, 50)
        lbl2 = MyLabel('Finestre / Porte Finestre', self, x_label, 100)
        self.chk1 = QtWidgets.QCheckBox("Sensore Marrone", self)
        self.chk1.setFixedWidth(310)
        self.chk1.move(x_label, 135)
        lbl3 = MyLabel('Disimpegni dell\' abitazione', self, x_label, 170)
        self.chk2 = QtWidgets.QCheckBox("Sensore Marrone", self)
        self.chk2.setFixedWidth(310)
        self.chk2.move(x_label, 205)
        lbl4 = MyLabel('Rilevatore di movimento', self, x_label, 250)
        lbl4_bis = MyLabel('(camera da letto, sala, cucina,...)', self, x_label, 275)
        lbl5 = MyLabel('Utenti del sistema di allarme', self, x_label, 325)
        lbl5_bis = MyLabel('(telecomandi)', self, x_label, 350)
        lbl6 = MyLabel('Terrazzi da proteggere', self, x_label, 400)
        lbl7 = MyLabel('Rivelatore di allagamento', self, x_label, 460)
        lbl8 = MyLabel('Rivelatore di fumo', self, x_label, 515)
        lbl9 = MyLabel('Rivelatore di monossido', self, x_label, 570)

        self.lblSum = QtWidgets.QLabel('', self)
        self.lblSum.move(x_entry-20, 650)
        sum_font = QtGui.QFont("Times", 12, QtGui.QFont.Bold)
        self.lblSum.setFont(sum_font)

        self.radio1 = RadioButtonPair(self)
        self.radio1.move(x_entry - 30, 450)
        self.radio2 = RadioButtonPair(self)
        self.radio2.move(x_entry - 30, 505)
        self.radio3 = RadioButtonPair(self)
        self.radio3.move(x_entry - 30, 560)
        self.all_radio = [self.radio1, self.radio2, self.radio3]
        for rb in self.all_radio:
            rb.b1.clicked.connect(lambda: self.onChanged(''))
            rb.b2.clicked.connect(lambda: self.onChanged(''))

        # QSpinBox potrebbe esser meglio
        self.entry1Edit = MyEntry(self, x_entry, 50, 1, 1, 4)
        self.entry2Edit = MyEntry(self, x_entry, 100, 0, 0, 20)
        self.entry3Edit = MyEntry(self, x_entry, 170, 1, 1, 4)
        self.entry4Edit = MyEntry(self, x_entry, 250, 0, 0, 10)
        self.entry5Edit = MyEntry(self, x_entry, 325, 1, 1, 5)
        self.entry6Edit = MyEntry(self, x_entry, 400, 0, 0, 4)
        self.all_entries = [self.entry1Edit, self.entry2Edit, self.entry3Edit, self.entry4Edit,
                            self.entry5Edit, self.entry6Edit]

        self.lastEntries = []
        for entry in self.all_entries:
            entry.textChanged[str].connect(self.onChanged)
            self.lastEntries.append(entry.text())

        line = QtWidgets.QFrame(self)
        line.setGeometry(x_entry-20, 630, 150, 3)
        # line.move(x_entry, 620)
        line.setFrameShape(QtWidgets.QFrame.HLine)

        self.lblContacts = QtWidgets.QLabel('Contatti:\nIng. Francesco Brigidi, Smart Security Srl \nVia della Cooperazione, 8/10, 47043 Gatteo (FC), T. 0541 942414', self)
        self.lblContacts.move(10, self.height()-100)
        self.lblContacts.setFixedWidth(self.width())
        self.lblContacts.setFixedHeight(70)
        contacts_font = QtGui.QFont("Times", 6, QtGui.QFont.Normal)
        self.lblContacts.setFont(contacts_font)

        footer = QtWidgets.QFrame(self)
        footer.setGeometry(0, self.height()-30, self.width(), 30)
        p = footer.palette()
        p.setColor(footer.backgroundRole(), QtGui.QColor(255, 255, 255))
        footer.setPalette(p)
        footer.setAutoFillBackground(True)
        footer.lower()

        self.onChanged(self.entry1Edit)
        self.show()

    def close_application(self):
        # Si potrebbe mettere un pop up sei sicuro di uscire
        self.removePdfs()
        sys.exit()

    def new_application(self):

        self.entry1Edit.setText("1")
        self.entry2Edit.setText("0")
        self.entry3Edit.setText("1")
        self.entry4Edit.setText("0")
        self.entry5Edit.setText("1")
        self.entry6Edit.setText("0")
        self.radio1.b1.setChecked(True)
        self.radio2.b1.setChecked(True)
        self.radio3.b1.setChecked(True)
        self.chk1.setChecked(False)
        self.chk2.setChecked(False)

        self.onChanged('')

    def exportPDF_application(self):

        #response = HttpResponse(content_type="application/pdf")
        #response['Content-Disposition']='filename="preventivo2.pdf"'
        #pdfcanvas = canvas.Canvas(response)

        formatted_time = time.ctime()

        pdf_name = time.strftime("%d_%m_%Y") + time.strftime("__%H_%M_%S") + ".pdf"
        doc = SimpleDocTemplate(pdf_name, pagesize=letter,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=18)
        Body = []
        logo = "logo.jpg"

        im = Image(logo, 2*inch, 2*inch)
        Body.append(im)
        Body.append(Spacer(1, 12))

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
        ptext = '<font size=12>%s</font>' % formatted_time
        Body.append(Paragraph(ptext, styles["Normal"]))
        Body.append(Spacer(1, 12))

        data = [['cosa 1', 1],
                ['cosa 2', 1]]
        table_col_width = 100
        table_row_height = 20
        t = Table(data, table_col_width, table_row_height)
        t.setStyle(TableStyle([('FONT', (0,0), (0, -1), 'Helvetica-Bold')]))
        Body.append(t)

        doc.build(Body)
        os.startfile(pdf_name)

    def onChanged(self, lastEntry):

        self.validateEntry(lastEntry)

        costante = 1100.0
        iva = 1.22

        porte_ingresso = 50.0
        finestre = 50.0
        disimpegni = 74.0
        sensore_movimento = 74.0
        telecomandi = 51.0
        terrazzi = 215.0
        rivelatore_allagamento = 74.0
        rivelatore_fumo = 108.0
        rivelatore_monossido = 174.0

        entries_int = []
        self.lastEntries = []
        for entry in self.all_entries:
            if entry.text() == '':
                entries_int.append(0)
                self.lastEntries.append('0')
            else:
                entries_int.append(float(entry.text()))
                self.lastEntries.append(entry.text())

        for rb in self.all_radio:
            if rb.b2.isChecked():
                entries_int.append(1)
            else:
                entries_int.append(0)

        moneySum = (entries_int[0] * porte_ingresso + entries_int[1] * finestre + entries_int[2] * disimpegni +
               entries_int[3] * sensore_movimento + entries_int[4] * telecomandi + entries_int[5] * terrazzi +
               entries_int[6] * rivelatore_allagamento + entries_int[7] * rivelatore_fumo +
               entries_int[8] * rivelatore_monossido + costante) * iva

        self.lblSum.setText('{0:.2f}'.format(moneySum))
        self.lblSum.adjustSize()

    def removePdfs(self):
        filelist = [f for f in os.listdir(".") if f.endswith(".pdf")]
        for f in filelist:
            os.remove(f)

    def closeEvent(self, event):
        self.removePdfs()
        event.accept()

    def validateEntry(self, txt):

        entries_sum = self.getAllEntriesSum()
        if entries_sum > self.maxSensorNbr:
            for ii, entry in enumerate(self.all_entries):
                entry.setText(self.lastEntries[ii])

    def getAllEntriesSum(self):

        entries_sum = 0
        for entry in self.all_entries:
            if entry.text() != '':
                entries_sum += int(entry.text())

        for rb in self.all_radio:
            if rb.b2.isChecked():
                entries_sum += 1

        return entries_sum


def run():
    app = QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

run()