import sys
from PyQt5.QtWidgets import *  # import VŠEHO z Pyqt5.QtWidgets

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()  # magie

		# vytvoření labelu (nápisu) a buttonu (tlačítka)
        self.label = QLabel("Pole: []")

        self.pole = []

        self.lineEdit = QLineEdit()

        self.button = QPushButton("Ukousni")
        self.button.clicked.connect(self.ukousni)

        self.button2 = QPushButton("Přidej")
        self.button2.clicked.connect(self.pridej)

        self.button3 = QPushButton("Vyčisti")
        self.button3.clicked.connect(self.vycisti)

        self.button4 = QPushButton("Obrať")
        self.button4.clicked.connect(self.obrat)

		# vytvoření vertikálního layoutu, který pokládá věci pod sebe
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.button)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        layout.addWidget(self.button4)

		# aplikování layoutu
        self.setLayout(layout)

		# ukázání widgetu
        self.show()
        
    def ukousni(self):
        if len(self.pole) != 0:
            self.pole.pop()

        self.label.setText("Pole: " + str(self.pole))

    def pridej(self):
        self.pole.append(self.lineEdit.text())

        self.label.setText("Pole: " + str(self.pole))

    def vycisti(self):
        self.pole = []

        self.label.setText("Pole: " + str(self.pole))

    def obrat(self):
        #self.pole = list(reversed(self.pole))

        for i in range(0, len(self.pole) // 2):
            opak_i = len(self.pole) - i - 1

            x = self.pole[i]
            self.pole[i] = self.pole[opak_i]
            self.pole[opak_i] = x

        self.label.setText("Pole: " + str(self.pole))

# magie
app = QApplication(sys.argv)
ex = MyWindow()
sys.exit(app.exec_())

