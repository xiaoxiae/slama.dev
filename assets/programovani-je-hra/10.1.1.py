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

            # aplikování layoutu
        self.setLayout(layout)

            # ukázání widgetu
        self.show()


    def stisknute_tlacitko(self):
        self.pocet_susenek += self.delta_susenek

        self.label.setText(str(self.pocet_susenek))

# magie
app = QApplication(sys.argv)
ex = MyWindow()
sys.exit(app.exec_())
