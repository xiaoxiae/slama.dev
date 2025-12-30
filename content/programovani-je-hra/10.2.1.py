import sys
from PyQt5.QtWidgets import *  # import VŠEHO z Pyqt5.QtWidgets


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()  # magie

        # vytvoření labelu (nápisu) a buttonu (tlačítka)
        self.label = QLabel("Délka: 0")

        self.lineEdit = QLineEdit()
        self.lineEdit.textChanged.connect(self.zmena_textu)

        self.button = QPushButton("Stiskni mě, lol.")
        self.button.clicked.connect(self.stisknute_tlacitko)

        self.button2 = QPushButton("Nemačkej mě, né lol.")
        self.button2.clicked.connect(self.stisknute_tlacitko2)

        # vytvoření vertikálního layoutu, který pokládá věci pod sebe
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.button)
        layout.addWidget(self.button2)

        # aplikování layoutu
        self.setLayout(layout)

        # ukázání widgetu
        self.show()

    def zmena_textu(self):
        self.label.setText("Délka: " + str(len(self.lineEdit.text())))

    def stisknute_tlacitko(self):
        self.lineEdit.setText(self.lineEdit.text() + "lol")

    def stisknute_tlacitko2(self):
        x = self.lineEdit.text()
        x = x[:-1]
        self.lineEdit.setText(x)


# magie
app = QApplication(sys.argv)
ex = MyWindow()
sys.exit(app.exec_())
