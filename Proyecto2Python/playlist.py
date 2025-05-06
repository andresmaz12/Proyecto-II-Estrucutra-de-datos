class nodoPlaylist:
    def __init__(self, cancion, ruta, artista, duracion):
        self.cancion = cancion
        self.ruta = ruta
        self.artista = artista
        self.duracion = duracion
        self.siguiente = None
        self.anterior = None
        self.listado = None

class linkedListPlaylist:
    def __init__(self):
            self.cabeza = None
            self.cola = None
            self.tamaño = 0
        
    def estaVacia(self):
            return self.cabeza is None
        
    def agregarCancion(self, cancion, ruta, artista, duracion):
            if isinstance(cancion, str):
                cancion_dict = {"titulo": cancion, "artista": artista, "duracion": duracion, "ruta": ruta}
            else:
                cancion_dict = cancion
                
            nuevoNodo = nodoPlaylist(cancion_dict, ruta, artista, duracion)
            
            if self.estaVacia():
                self.cabeza = nuevoNodo
                self.cola = nuevoNodo

                nuevoNodo.siguiente = nuevoNodo
                nuevoNodo.anterior = nuevoNodo
            else:
                nuevoNodo.anterior = self.cola
                nuevoNodo.siguiente = self.cabeza
                self.cola.siguiente = nuevoNodo
                self.cabeza.anterior = nuevoNodo
                self.cola = nuevoNodo
            
            self.tamaño += 1
            return nuevoNodo
        
    def eliminarCancion(self, titulo):
            if self.estaVacia():
                return False
            
            actual = self.cabeza
            encontrado = False

            while True:
                if actual.cancion["titulo"] == titulo:
                    encontrado = True
                    break
                actual = actual.siguiente
                if actual == self.cabeza:
                    break
            
            if not encontrado:
                return False

            if self.tamaño == 1:
                self.cabeza = None
                self.cola = None
            else:

                if actual == self.cabeza:
                    self.cabeza = actual.siguiente

                if actual == self.cola:
                    self.cola = actual.anterior

                actual.anterior.siguiente = actual.siguiente
                actual.siguiente.anterior = actual.anterior
            
            self.tamaño -= 1
            return True
        
    def buscarCancion(self, titulo):
            if self.estaVacia():
                return None
            
            actual = self.cabeza
            
            while True:
                if actual.cancion["titulo"] == titulo:
                    return actual.cancion
                actual = actual.siguiente
                if actual == self.cabeza:
                    break
            
            return None
        
    def mostrarCanciones(self):
        if self.estaVacia():
            print("La lista de canciones está vacía")
            return []
        
        canciones = []
        actual = self.cabeza
        contador = 1
    

    def siguienteCancion(self, nodo_actual):
            return nodo_actual.siguiente
        
    def cancionAnterior(self, nodo_actual):
            return nodo_actual.anterior