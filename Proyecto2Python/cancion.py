import os
import pickle
from tkinter import messagebox

class NodoCancion:
    def __init__(self, cancion, ruta, artista, duracion):
        self.cancion = cancion
        self.ruta = ruta
        self.artista = artista
        self.duracion = duracion
        self.siguiente = None  

class ListaCanciones:
    def __init__(self):
        self.cabeza = None
        self.cola = None  
        self.tamaño = 0

    def estaVacia(self):
        return self.cabeza is None
    
    def agregarCancion(self, cancion, ruta, artista, duracion):
        try:
            # Validar estructura de la canción
            if not isinstance(cancion, dict):
                raise ValueError("La canción debe ser un diccionario")
            
            if 'titulo' not in cancion:
                raise ValueError("La canción debe tener un título")
            
            # Crear nuevo nodo
            nuevoNodo = NodoCancion(cancion, ruta, artista, duracion)
            
            if self.estaVacia():
                self.cabeza = nuevoNodo
                self.cola = nuevoNodo
            else:
                self.cola.siguiente = nuevoNodo
                self.cola = nuevoNodo
            
            self.tamaño += 1
            return nuevoNodo
        
        except Exception as e:
            print(f"Error en agregarCancion: {str(e)}")
            return None
    
    def eliminarCancion(self, titulo):
        if self.estaVacia():
            return False
        
        actual = self.cabeza
        anterior = None
        encontrado = False

        while actual is not None:
            if actual.cancion["titulo"] == titulo:
                encontrado = True
                break
            anterior = actual
            actual = actual.siguiente
        
        if not encontrado:
            return False

        if anterior is None:  
            self.cabeza = actual.siguiente
            if self.cabeza is None:  
                self.cola = None
        else:
            anterior.siguiente = actual.siguiente
            if actual.siguiente is None:  
                self.cola = anterior
        
        self.tamaño -= 1
        return True
    
    def buscarCancion(self, titulo):
        actual = self.cabeza
        
        while actual is not None:
            if 'titulo' in actual.cancion and actual.cancion['titulo'] == titulo:
                return actual
            actual = actual.siguiente
        
        return None
    
    def mostrarCanciones(self):
        if self.estaVacia():
            return []
        
        actual = self.cabeza
        contador = 1
        canciones = []
        
        while actual is not None:
            titulo = actual.cancion.get('titulo', 'Desconocido')
            artista = actual.cancion.get('artista', 'Desconocido')
            
            texto = f"{contador}. {titulo} - {artista}"
            canciones.append(texto)
            actual = actual.siguiente
            contador += 1
        
        return canciones

    def siguienteCancion(self, nodoActual):
        return nodoActual.siguiente if nodoActual else None
    
    def guardarPlaylist(self, nombreArchivo):
        try:
            datos = []
            actual = self.cabeza
            
            while actual is not None:
                datos.append({
                    'cancion': actual.cancion,
                    'ruta': actual.ruta,
                    'artista': actual.artista,
                    'duracion': actual.duracion
                })
                actual = actual.siguiente

            with open(nombreArchivo, 'wb') as archivo:
                pickle.dump(datos, archivo)
            
            return True
        except Exception as e:
            print(f"Error al guardar la playlist: {e}")
            return False
    
    def cargarPlaylist(self, nombreArchivo):
        try:
            if not os.path.exists(nombreArchivo):
                print(f"El archivo {nombreArchivo} no existe.")
                return False
            
            self.cabeza = None
            self.cola = None
            self.tamaño = 0

            with open(nombreArchivo, 'rb') as archivo:
                datos = pickle.load(archivo)

            for dato in datos:
                self.agregarCancion(
                    dato['cancion'],
                    dato['ruta'],
                    dato['artista'],
                    dato['duracion']
                )
            
            return True
        except Exception as e:
            print(f"Error al cargar la playlist: {e}")
            return False