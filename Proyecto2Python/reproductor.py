import pygame
import os
import time
from threading import Thread
from tkinter import messagebox  

from playlist import linkedListPlaylist

class ReproductorAudio:
    def __init__(self, playlist=None):
        self._playlist = playlist if playlist is not None else linkedListPlaylist()
        self.cancionActual = None
        self.reproduciendo = False
        self.hiloReproduccion = None
        self.pausado = False
        self.modoReproduccion = "normal"  
        
        pygame.mixer.init()
    
    @property
    def playlist(self):
        return self._playlist
        
    @playlist.setter
    def playlist(self, valor):
        if valor is None:
            valor = linkedListPlaylist()
        self._playlist = valor
        
    def cargarLista(self, listaReproduccion):
        if self.reproduciendo:
            self.detener()

        self._playlist = listaReproduccion
        self.cancionActual = self._playlist.cabeza if not self._playlist.estaVacia() else None
    
    def _reproducirCancion(self, rutaArchivo):
        try:
            if not os.path.exists(rutaArchivo):
                raise FileNotFoundError(f"Archivo no encontrado: {rutaArchivo}")

            extension = os.path.splitext(rutaArchivo)[1].lower()
            if extension not in ['.mp3', '.wav', '.ogg']:
                raise ValueError(f"Formato no soportado: {extension}")
            
            pygame.mixer.music.load(rutaArchivo)
            pygame.mixer.music.play()
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo reproducir {os.path.basename(rutaArchivo)}: {str(e)}")
            print(f"Error detallado: {traceback.format_exc()}")    
            
    def _iniciarHiloReproduccion(self):
        if self.cancionActual and 'ruta' in self.cancionActual.cancion:
            self.hiloReproduccion = Thread(
                target=self._reproducirCancion, 
                args=(self.cancionActual.ruta,)
            )
            self.hiloReproduccion.daemon = True
            self.hiloReproduccion.start()
    
    def iniciarReproduccion(self):
        if self._playlist.estaVacia():
            messagebox.showwarning("Advertencia", "No hay canciones en la lista de reproducción")
            return False
        
        if self.cancionActual is None:
            self.cancionActual = self._playlist.cabeza
        
        if not hasattr(self.cancionActual, 'ruta') or not self.cancionActual.ruta:
            messagebox.showwarning("Advertencia", f"La canción {self.cancionActual.cancion['titulo']} no tiene una ruta de archivo válida")
            return False
            
        if self.pausado:
            pygame.mixer.music.unpause()
            self.pausado = False
        else:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            
            self.reproduciendo = True
            self._iniciarHiloReproduccion()
        
        messagebox.showinfo("Reproduciendo", 
                          f"Reproduciendo: {self.cancionActual.cancion['titulo']} - "
                          f"{self.cancionActual.cancion['artista']} "
                          f"({self.cancionActual.cancion['duracion']})")
        return True
    
    def pausar(self):
        if not self.pausado and self.reproduciendo:
            pygame.mixer.music.pause()
            self.pausado = True
            messagebox.showinfo("Pausado", f"Pausado: {self.cancionActual.cancion['titulo']}")
            return True
        else:
            messagebox.showwarning("Advertencia", "No hay reproducción para pausar")
            return False   
    
    def detener(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        
        self.reproduciendo = False
        self.pausado = False
        messagebox.showinfo("Detenido", "Reproducción detenida")
        return True
    
    def siguiente(self, auto=False):
        if self._playlist.estaVacia() or self.cancionActual is None:
            messagebox.showwarning("Advertencia", "No hay canciones en la lista de reproducción")
            return False
        
        estabaReproduciendo = self.reproduciendo and not self.pausado
        
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        
        self.cancionActual = self._playlist.siguienteCancion(self.cancionActual)
        messagebox.showinfo("Siguiente", 
                          f"Canción siguiente: {self.cancionActual.cancion['titulo']} - "
                          f"{self.cancionActual.cancion['artista']}")
        
        if estabaReproduciendo or auto:
            self.pausado = False
            self.reproduciendo = True
            self._iniciarHiloReproduccion()
        
        return True
    
    def anterior(self):
        if self._playlist.estaVacia() or self.cancionActual is None:
            messagebox.showwarning("Advertencia", "No hay canciones en la lista de reproducción")
            return False
        
        estabaReproduciendo = self.reproduciendo and not self.pausado
        
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        
        self.cancionActual = self._playlist.cancionAnterior(self.cancionActual)
        messagebox.showinfo("Anterior", 
                          f"Canción anterior: {self.cancionActual.cancion['titulo']} - "
                          f"{self.cancionActual.cancion['artista']}")
        
        if estabaReproduciendo:
            self.pausado = False
            self.reproduciendo = True
            self._iniciarHiloReproduccion()
        
        return True
    
    def cambiarModo(self, modo):
        modosValidos = ["normal", "repetir", "aleatorio"]
        if modo not in modosValidos:
            messagebox.showwarning("Advertencia", 
                                  f"Modo no válido. Modos disponibles: {', '.join(modosValidos)}")
            return False
        
        self.modoReproduccion = modo
        messagebox.showinfo("Modo cambiado", f"Modo de reproducción cambiado a: {modo}")
        return True
    
    def buscarYReproducir(self, titulo):
        if self._playlist.estaVacia():
            messagebox.showwarning("Advertencia", "No hay canciones en la lista de reproducción")
            return False
        
        nodoEncontrado = self._playlist.buscarCancion(titulo)
        
        if not nodoEncontrado:
            messagebox.showwarning("No encontrado", 
                                  f"No se encontró la canción '{titulo}' en la lista de reproducción")
            return False

        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        
        self.cancionActual = nodoEncontrado
        messagebox.showinfo("Canción encontrada", 
                          f"Canción encontrada: {self.cancionActual.cancion['titulo']} - "
                          f"{self.cancionActual.cancion['artista']}")
        
        self.pausado = False
        self.reproduciendo = True
        self._iniciarHiloReproduccion()
        
        return True
    
    def ajustarVolumen(self, nivel): 
        pygame.mixer.music.set_volume(nivel)
        messagebox.showinfo("Volumen ajustado", f"Volumen ajustado a: {nivel*100:.0f}%")
        return True