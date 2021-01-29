class Clovek:

	def __init__(self, jmeno, vek, vaha):
		self.jmeno = jmeno
		self.vek = vek
		self.vaha = vaha

	def vyrost(self):
		self.vek += 1

	def ztloustni(self):
		self.vaha += 1

	def zhubni(self):
		self.vaha += 1
