import numpy as np

g = 9.81 #kg*m/s^2


class Barra(object):

	"""Constructor para una barra"""
	def __init__(self, ni, nj, R, t, E, ρ, σy):
		super(Barra, self).__init__()
		self.ni = ni
		self.nj = nj
		self.R = R
		self.t = t
		self.E = E
		self.ρ = ρ
		self.σy = σy

	def obtener_conectividad(self):
		return [self.ni, self.nj]

	def calcular_area(self):
		A = np.pi*(self.R**2 - (self.R-self.t)**2)
		return A

	def calcular_largo(self, reticulado):
		xi = reticulado.obtener_coordenada_nodal(self.ni)
		xj = reticulado.obtener_coordenada_nodal(self.nj)
		dij = xi - xj
		return np.sqrt(np.dot(dij,dij))

	def calcular_peso(self, reticulado):
		L = self.calcular_largo(reticulado)
		A = self.calcular_area()
		return self.ρ * A * L * g

	def obtener_rigidez(self, reticulado) :
		L = self.calcular_largo(reticulado)
		A = self.calcular_area()
		k = self.E * A / L
		
		xi = reticulado.obtener_coordenada_nodal(self.ni)
		xj = reticulado.obtener_coordenada_nodal(self.nj)
		resta_coordenadas = xj - xi
		cosθ = resta_coordenadas[0] / L
		sinθ = resta_coordenadas[1] / L
		Tθ = np.array([[-cosθ, -sinθ, cosθ, sinθ]])
		
		Ke = k* Tθ.T @ Tθ
		return Ke # matriz (4x4)

	def obtener_vector_de_cargas(self, reticulado):
		w = self.calcular_peso(reticulado)
		vector = np.array([[0, -1, 0, -1]])
		fe = vector.T * w/2
		return fe # Vector numpy de (4x1)

	def obtener_fuerza(self, reticulado):
		L = self.calcular_largo(reticulado)
		A = self.calcular_area()
		k = self.E * A / L
		
		xi = reticulado.obtener_coordenada_nodal(self.ni)
		xj = reticulado.obtener_coordenada_nodal(self.nj)
		resta_coordenadas = xj - xi
		cosθ = resta_coordenadas[0] / L
		sinθ = resta_coordenadas[1] / L
		Tθ = np.array([[-cosθ, -sinθ, cosθ, sinθ]])
		
		ui = reticulado.obtener_desplazamiento_nodal(self.ni)
		uj = reticulado.obtener_desplazamiento_nodal(self.nj)
		vector_ue = np.array([ui[0], ui[1],uj[0],uj[1]]) # Vector numpy de (4x1)

		# delta = Tθ · ue
		delta = Tθ @ vector_ue
		se = k * delta
		return se[0] # Escalar
	






