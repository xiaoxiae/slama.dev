class Clovek:
    def __init__(self, jmeno, vek):
        self.jmeno = jmeno
        self.vek = vek

    def vyrost(self):
        self.vek += 1

    def vyrost_o(self, o):
        self.vek += o
