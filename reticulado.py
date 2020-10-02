import numpy as np
from scipy.linalg import solve

class Reticulado(object):
	"""Define un reticulado"""
	__NNodosInit__ = 100
	def __init__(self):
		super(Reticulado, self).__init__()
		
		self.xyz = np.zeros((Reticulado.__NNodosInit__,3), dtype=np.double)
		self.Nnodos = 0
		self.barras = []
		self.cargas = {}
		self.restricciones = {}
		self.Ndimensiones = 2
		self.tiene_solucion = False
		
	def agregar_nodo(self, x, y, z=0):
		if self.Nnodos+1 > Reticulado.__NNodosInit__:
			self.xyz.resize((self.Nnodos+1,3))
		self.xyz[self.Nnodos,:] = [x,y,z]
		self.Nnodos +=1
		if z != 0.:
			self.Ndimensiones = 3
		
	def agregar_barra(self, barra):
		self.barras.append(barra)
		
	def obtener_coordenada_nodal(self, n): 
		if n >= self.Nnodos :
			return
		return self.xyz[n, :]
		
	def calcular_peso_total(self):
		peso = 0
		for b in self.barras :
			peso += barra.calcular_peso(self)
		return peso
		
	def obtener_nodos(self):
		return self.xyz[0:self.Nnodos,:].copy()
		
	def obtener_barras(self):
		return self.barras
	
	def agregar_restriccion(self, nodo, gdl, valor=0.0):
		if nodo not in self.restricciones:
			self.restricciones[nodo] = [[gdl, valor]]
		else:
			self.restricciones[nodo].append([gdl, valor])
			
	def agregar_fuerza(self, nodo, gdl, valor):
		if nodo not in self.cargas:
			self.cargas[nodo] = [[gdl, valor]]
		else:
			self.cargas[nodo].append([gdl, valor])
			
	def ensamblar_sistema(self):
		Ngdl = self.Nnodos * self.Ndimensiones
		
		self.K = np.zeros((Ngdl,Ngdl), dtype=np.double)
		self.f = np.zeros((Ngdl), dtype=np.double)
		self.u = np.zeros((Ngdl), dtype=np.double)
		
		for b in self.barras:
			ke = b.obtener_rigidez(self)
			fe = b.obtener_vector_de_cargas(self)
			nodos = b.obtener_conectividad()
			d = np.array([ 2*nodos[0] , 2*nodos[0]+1 , 2*nodos[1] , 2*nodos[1]+1 ])
			
			for i in range(4):
				p = d[i]
				for j in range(4):
					q = d[j]
					self.K[p,q] += ke[i,j]
				self.f[p] += fe[j]
	
	def resolver_sistema(self):
		Ngdl = self.Nnodos * self.Ndimensiones
		gdl_libres = np.arange(Ngdl)
		gdl_restringidos = []
		
		for nodo in self.restricciones:
			for restriccion in self.restricciones[nodo]:
				gdl_local = restriccion[0]
				valor = restriccion[1]
				
				gdl_global = 2*nodo + gdl_local
				gdl_restringidos.append(gdl_global)
				self.u[gdl_global] = valor
		
		gdl_final = np.setdiff1d(gdl_libres,gdl_restringidos)
		
		for nodo in self.cargas:
			for carga in self.cargas[nodo]:
				gdl = carga[0]
				valor = carga[1]
				gdl_global = 2*nodo + gdl
				
				self.f[gdl_global] += valor
				
		Kff = self.K[np.ix_(gdl_final,gdl_final)]
		Kcf = self.K[np.ix_(gdl_restringidos,gdl_final)]
		Kfc = Kcf.T
		Kcc = self.K[np.ix_(gdl_restringidos,gdl_restringidos)]
		
		uf = self.u[gdl_final]
		uc = self.u[gdl_restringidos]
		
		ff = self.f[gdl_final]
		fc = self.f[gdl_restringidos]
		
		uf = solve(Kff, ff - Kfc @ uc)
		
		self.Rc = Kcf@uf + Kcc@uc - fc
		# Resolver para obtener uf -->  Kff uf = ff - Kfc*uc
		
		#Asignar uf al vector solucion
		self.u[gdl_final] = uf
		
		#Marcar internamente que se tiene solucion
		self.tiene_solucion = True
		
		
	def obtener_desplazamiento_nodal(self, n):
		dofs = [2*n, 2*n+1]
		return self.u[dofs]
	
	def recuperar_fuerzas(self):
		fuerzas = np.zeros((len(self.barras)), dtype=np.double)
		for i,b in enumerate(self.barras):
			fuerzas[i] = b.obtener_fuerza(self)
		return fuerzas
	
	
	def __str__(self):
		s = "nodos:\n"
		for n in range(self.Nnodos):
			s += f"  {n} : ( {self.xyz[n,0]}, {self.xyz[n,1]}, {self.xyz[n,2]}) \n "
		s += "\n\n"
		
		s += "barras:\n"
		for i, b in enumerate(self.barras):
			n = b.obtener_conectividad()
			s += f" {i} : [ {n[0]} {n[1]} ] \n"
		s += "\n\n"
		
		s += "restricciones:\n"
		for nodo in self.restricciones:
			s += f"{nodo} : {self.restricciones[nodo]}\n"
		s += "\n\n"
		
		s += "cargas:\n"
		for nodo in self.cargas:
			s += f"{nodo} : {self.cargas[nodo]}\n"
		s += "\n\n"
		
		if self.tiene_solucion:
			s += "desplazamientos:\n"
			if self.Ndimensiones == 2:
				uvw = self.u.reshape((-1,2))
				for n in range(self.Nnodos):
					s += f"  {n} : ( {uvw[n,0]}, {uvw[n,1]}) \n "
		s += "\n\n"
		
		if self.tiene_solucion:
			f = self.recuperar_fuerzas()
			s += "fuerzas:\n"
			for b in range(len(self.barras)):
				s += f"  {b} : {f[b]}\n"
		s += "\n"
		
		return s
