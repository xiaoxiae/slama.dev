import sys
from PyQt5.QtWidgets import *  # import VŠEHO z Pyqt5.QtWidgets

class MyWindow(QWidget):


    def __init__(self):
        super().__init__()  # magie

		    # vytvoření labelu (nápisu) a buttonu (tlačítka)
        self.label = QLabel('0')
        self.button = QPushButton('Keksík.')
        self.button.clicked.connect(self.stisknute_tlacitko)

        self.pocet_susenek = 0
        self.delta_susenek = 1

		    # vytvoření vertikálního layoutu, který pokládá věci pod sebe
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        horizontal_layout = QHBoxLayout()

        self.b1 = QPushButton('10')
        self.b1.clicked.connect(self.b1_funkce)
        self.b2 = QPushButton('100')
        self.b2.clicked.connect(self.b2_funkce)
        self.b3 = QPushButton('1000')
        self.b3.clicked.connect(self.b3_funkce)

        self.b1.setEnabled(False)
        self.b2.setEnabled(False)
        self.b3.setEnabled(False)

        horizontal_layout.addWidget(self.b1)
        horizontal_layout.addWidget(self.b2)
        horizontal_layout.addWidget(self.b3)

        layout.addLayout(horizontal_layout)

		    # aplikování layoutu
        self.setLayout(layout)

		    # ukázání widgetu
        self.show()


    def stisknute_tlacitko(self):
        self.pocet_susenek += self.delta_susenek

        self.label.setText(str(self.pocet_susenek))

        self.zkontroluj_tlacitka()


    def b1_funkce(self):
        self.pocet_susenek -= 10
        self.delta_susenek += 1

        self.label.setText(str(self.pocet_susenek))

        self.zkontroluj_tlacitka()

    def b2_funkce(self):
        self.pocet_susenek -= 100
        self.delta_susenek += 5

        self.label.setText(str(self.pocet_susenek))

        self.zkontroluj_tlacitka()

    def b3_funkce(self):
        self.pocet_susenek -= 1000
        self.delta_susenek += 25

        self.label.setText(str(self.pocet_susenek))

        self.zkontroluj_tlacitka()

    def zkontroluj_tlacitka(self):
        if self.pocet_susenek >= 10:
          self.b1.setEnabled(True)
        else:
          self.b1.setEnabled(False)

        if self.pocet_susenek >= 100:
          self.b2.setEnabled(True)
        else:
          self.b2.setEnabled(False)
          
        if self.pocet_susenek >= 1000:
          self.b3.setEnabled(True)
        else:
          self.b3.setEnabled(False)


# magie
app = QApplication(sys.argv)
ex = MyWindow()
sys.exit(app.exec_())
