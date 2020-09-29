import numpy as np

class Reticulado(object):
	"""Define un reticulado"""
	def __init__(self):
		super(Reticulado, self).__init__()
		
		self.xyz = np.zeros((0,3), dtype=np.double)
		self.Nnodos = 0
		self.barras = []
		self.cargas = {}
		self.restricciones = {}

	def agregar_nodo(self, x, y, z=0):
		self.xyz.resize((self.Nnodos+1,3))
		self.xyz[self.Nnodos,:] = [x,y,z]
		self.Nnodos += 1
		return
		
	def agregar_barra(self, barra):
		return self.barras.append(barra)
		
	def obtener_coordenada_nodal(self, n): 
		if n >= self.Nnodos :
			return
		return self.xyz[n, :]
		
	def calcular_peso_total(self):
		peso = 0
		for barra in self.barras :
			peso += barra.calcular_peso(self)
		return peso
		
	def obtener_nodos(self):
		return self.xyz 
		
	def obtener_barras(self):
		return self.barras 

	def agregar_restriccion(self, nodo, gdl, valor=0.0):
		"""Implementar"""
		return

	def agregar_fuerza(self, nodo, gdl, valor):
		"""Implementar"""
		return

	def ensamblar_sistema(self):
		"""Implementar"""
		return

	def resolver_sistema(self):
		"""Implementar"""
		return

	def recuperar_fuerzas(self):
		"""Implementar"""
		return

	
	def __str__(self):
		s = "nodos:\n"
		for n in range(self.Nnodos) :
			s += f" {n} : ( {self.xyz[n][0]}, {self.xyz[n][1]}, {self.xyz[n][2]})\n"
		s += "\n\n"
		s += "barras:\n"
		
		for i, b in enumerate(self.barras) :
			n = b.obtener_conectividad()
			s += f" {i} : [ {n[0]} {n[1]} ] \n"
		return s
	
