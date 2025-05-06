import os
import pickle
import re
import traceback  # Añadido traceback
import pygame
from tkinter import messagebox
from cancion import ListaCanciones
from playlist import linkedListPlaylist
from reproductor import ReproductorAudio

class ManejoPrincipal:
    def __init__(self):
        self.listaCanciones = ListaCanciones()
        self.reproductor = ReproductorAudio()
        self.playlistActual = linkedListPlaylist()
        
    # Métodos para manejar canciones
    def agregarCancion(self, nombre, artista, duracion, ruta):
        try:
            # Normalizar ruta y verificar existencia
            ruta = os.path.normpath(ruta)
            if not os.path.exists(ruta):
                raise FileNotFoundError(f"El archivo no existe: {ruta}")
            
            # Validar campos obligatorios
            if not nombre.strip():
                raise ValueError("El nombre de la canción no puede estar vacío")
            
            # Crear estructura de canción
            cancion = {
                'titulo': nombre.strip(),
                'artista': artista.strip() if artista else "Desconocido",
                'duracion': duracion.strip() if duracion else "0:00",
                'ruta': ruta
            }
            
            # Agregar a la lista de canciones
            resultado = self.listaCanciones.agregarCancion(cancion, ruta, cancion['artista'], cancion['duracion'])
            
            if not resultado:
                raise RuntimeError("No se pudo agregar la canción a la lista")
            
            return True
        
        except Exception as e:
            print(f"Error al agregar canción: {str(e)}")
            messagebox.showerror("Error", f"No se pudo agregar la canción:\n{str(e)}")
            return False
    
    def eliminarCancion(self, titulo):
        return self.listaCanciones.eliminarCancion(titulo)
    
    def buscarCancion(self, titulo):
        return self.listaCanciones.buscarCancion(titulo)
    
    def obtenerListaCanciones(self):
        return self.listaCanciones.mostrarCanciones()
    
    # Métodos para manejar playlists
    def crearPlaylist(self, nombre):
        self.playlistActual = linkedListPlaylist()
        return True

    def agregarCancionAPlaylist(self, titulo):
        try:
            # Buscar la canción en la lista de canciones
            nodo_cancion = self.listaCanciones.buscarCancion(titulo)
            
            if not nodo_cancion:
                print(f"No se encontró la canción '{titulo}' en la lista")
                return False
                
            # Extraer la información necesaria
            cancion_info = {
                'titulo': nodo_cancion.cancion.get('titulo', 'Desconocido'),
                'artista': nodo_cancion.cancion.get('artista', 'Desconocido'),
                'duracion': nodo_cancion.cancion.get('duracion', '0:00'),
                'ruta': nodo_cancion.ruta
            }
            
            # Agregar a la playlist
            resultado = self.playlistActual.agregarCancion(
                cancion_info, 
                nodo_cancion.ruta, 
                cancion_info['artista'], 
                cancion_info['duracion']
            )
            
            return resultado is not None
        except Exception as e:
            print(f"Error al agregar canción a playlist: {str(e)}")
            print(traceback.format_exc())
            return False
    
    def eliminarCancionDePlaylist(self, titulo):
        try:
            return self.playlistActual.eliminarCancion(titulo)
        except Exception as e:
            print(f"Error al eliminar canción de playlist: {str(e)}")
            print(traceback.format_exc())
            return False
    
    def obtenerPlaylistActual(self):
        return self.playlistActual.mostrarCanciones()
    
    # Métodos para el reproductor
    def reproducir(self, titulo=None):
        try:
            if not titulo:
                return False
                
            # Buscar la canción en la lista principal
            nodo_cancion = self.listaCanciones.buscarCancion(titulo)
            if not nodo_cancion:
                print(f"No se encontró la canción '{titulo}' en la lista principal")
                return False
                
            # Verificar si ya está en la playlist o agregarla
            if self.playlistActual.estaVacia():
                # Si la playlist está vacía, agregar la canción
                nodo_playlist = self.playlistActual.agregarCancion(
                    nodo_cancion.cancion,
                    nodo_cancion.ruta,
                    nodo_cancion.artista,
                    nodo_cancion.duracion
                )
                self.reproductor.cancionActual = nodo_playlist
            else:
                # Buscar si ya existe en la playlist
                encontrada = False
                actual = self.playlistActual.cabeza
                
                while True:
                    if actual.cancion["titulo"] == titulo:
                        self.reproductor.cancionActual = actual
                        encontrada = True
                        break
                    actual = actual.siguiente
                    if actual == self.playlistActual.cabeza:
                        break
                
                # Si no está en la playlist, agregarla
                if not encontrada:
                    nodo_playlist = self.playlistActual.agregarCancion(
                        nodo_cancion.cancion,
                        nodo_cancion.ruta,
                        nodo_cancion.artista,
                        nodo_cancion.duracion
                    )
                    self.reproductor.cancionActual = nodo_playlist
            
            return self.reproductor.iniciarReproduccion()
            
        except Exception as e:
            print(f"Error al reproducir: {str(e)}")
            print(traceback.format_exc())
            return False
    
    def pausar(self):
        return self.reproductor.pausar()
    
    def detener(self):
        return self.reproductor.detener()
    
    def siguiente(self):
        return self.reproductor.siguiente()
    
    def anterior(self):
        return self.reproductor.anterior()
    
    def ajustarVolumen(self, nivel):
        return self.reproductor.ajustarVolumen(nivel)
    
    # Métodos para guardar/recuperar datos
    def guardarDatos(self, archivo):
        try:
            datos = {
                'canciones': self.listaCanciones,
                'playlists': self.playlistActual
            }
            with open(archivo, 'wb') as f:
                pickle.dump(datos, f)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron guardar los datos: {str(e)}")
            return False
    
    def cargarDatos(self, archivo):
        try:
            with open(archivo, 'rb') as f:
                datos = pickle.load(f)
            self.listaCanciones = datos.get('canciones', ListaCanciones())
            self.playlistActual = datos.get('playlists', linkedListPlaylist())
            return True
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los datos: {str(e)}")
            return False