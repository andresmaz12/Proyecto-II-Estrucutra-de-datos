import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import pygame
import traceback  # Añadido traceback
from pygame import mixer
from metodoMain import ManejoPrincipal
from playlist import linkedListPlaylist

class ReproductorMusica:
    def __init__(self, root):
        try:
            # Inicializar pygame solo una vez
            if not pygame.get_init():
                pygame.init()
                pygame.mixer.init()
                print("Pygame inicializado correctamente")
            
            self.root = root
            self.manejo_principal = ManejoPrincipal()
            self.setup_ui()
            self.reproduciendo = False
            self.cancion_actual = None
        
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo inicializar el reproductor: {str(e)}")
            print(f"Error de inicialización: {traceback.format_exc()}")
            raise
        
        # Variables de estado
        self.reproduciendo = False
        self.cancion_actual = None
        
    def setup_ui(self):
        self.root.title("Reproductor de Música")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")
        
        # Frames
        self.frame_superior = tk.Frame(self.root, bg="#f0f0f0")
        self.frame_superior.pack(pady=10)
        
        self.frame_medio = tk.Frame(self.root, bg="#f0f0f0")
        self.frame_medio.pack(pady=10)
        
        self.frame_botones = tk.Frame(self.root, bg="#f0f0f0")
        self.frame_botones.pack(pady=10)
        
        self.frame_playlist = tk.Frame(self.root, bg="#f0f0f0")
        self.frame_playlist.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Elementos de UI
        self.lbl_cancion_actual = tk.Label(self.frame_superior, text="No hay canción seleccionada", 
                                         font=("Arial", 12), bg="#f0f0f0", width=40)
        self.lbl_cancion_actual.pack(pady=5)
        
        self.lbl_canciones = tk.Label(self.frame_medio, text="Canciones:", font=("Arial", 10), bg="#f0f0f0")
        self.lbl_canciones.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.combo_canciones = ttk.Combobox(self.frame_medio, width=50, state="readonly")
        self.combo_canciones.grid(row=0, column=1, padx=5, pady=5)
        self.combo_canciones.bind("<<ComboboxSelected>>", self.seleccionar_cancion)
        
        # Botones principales
        self.btn_agregar = tk.Button(self.frame_botones, text="Agregar Canciones", 
                                   command=self.agregar_canciones, width=15, bg="#4CAF50", fg="white")
        self.btn_agregar.grid(row=0, column=0, padx=5, pady=5)
        
        self.btn_anterior = tk.Button(self.frame_botones, text="Anterior", 
                                    command=self.cancion_anterior, width=10, bg="#2196F3", fg="white")
        self.btn_anterior.grid(row=0, column=1, padx=5, pady=5)
        
        self.btn_reproducir = tk.Button(self.frame_botones, text="Reproducir", 
                                      command=self.reproducir_pausar, width=10, bg="#2196F3", fg="white")
        self.btn_reproducir.grid(row=0, column=2, padx=5, pady=5)
        
        self.btn_siguiente = tk.Button(self.frame_botones, text="Siguiente", 
                                     command=self.cancion_siguiente, width=10, bg="#2196F3", fg="white")
        self.btn_siguiente.grid(row=0, column=3, padx=5, pady=5)
        
        self.btn_crear_playlist = tk.Button(self.frame_botones, text="Crear Playlist", 
                                          command=self.crear_playlist, width=15, bg="#FF9800", fg="white")
        self.btn_crear_playlist.grid(row=0, column=4, padx=5, pady=5)
        
        # Playlist
        self.lbl_playlist = tk.Label(self.frame_playlist, text="Playlist:", font=("Arial", 10), bg="#f0f0f0")
        self.lbl_playlist.pack(anchor="w", padx=10)
        
        self.frame_lista_playlist = tk.Frame(self.frame_playlist, bg="white", bd=1, relief=tk.SUNKEN)
        self.frame_lista_playlist.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.listbox_playlist = tk.Listbox(self.frame_lista_playlist, selectmode=tk.SINGLE, width=60, height=8)
        self.listbox_playlist.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.scrollbar_playlist = tk.Scrollbar(self.frame_lista_playlist)
        self.scrollbar_playlist.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox_playlist.config(yscrollcommand=self.scrollbar_playlist.set)
        self.scrollbar_playlist.config(command=self.listbox_playlist.yview)
        
        # Botones de playlist
        self.frame_botones_playlist = tk.Frame(self.frame_playlist, bg="#f0f0f0")
        self.frame_botones_playlist.pack(pady=5, fill=tk.X)
        
        self.btn_borrar_cancion = tk.Button(self.frame_botones_playlist, text="Borrar Canción", 
                                          command=self.borrar_cancion_playlist, bg="#F44336", fg="white")
        self.btn_borrar_cancion.pack(side=tk.LEFT, padx=10)
        
        self.btn_borrar_playlist = tk.Button(self.frame_botones_playlist, text="Borrar Playlist", 
                                           command=self.borrar_playlist, bg="#F44336", fg="white")
        self.btn_borrar_playlist.pack(side=tk.LEFT, padx=10)
    
    def agregar_canciones(self):
        archivos = filedialog.askopenfilenames(
            title="Seleccionar archivos de música",
            filetypes=(("Archivos MP3", "*.mp3"), ("Archivos WAV", "*.wav"), ("Todos los archivos", "*.*"))
        )
        
        if archivos:
            for archivo in archivos:
                try:
                    # Normalizar la ruta y manejar caracteres especiales
                    ruta_normalizada = os.path.normpath(archivo)
                    nombre = os.path.splitext(os.path.basename(ruta_normalizada))[0]
                    
                    # Extraer artista y título si está en formato "Artista - Título"
                    if ' - ' in nombre:
                        artista, titulo = nombre.split(' - ', 1)
                    else:
                        artista = "Desconocido"
                        titulo = nombre
                    
                    # Agregar la canción
                    if self.manejo_principal.agregarCancion(titulo, artista, "0:00", ruta_normalizada):
                        print(f"Canción agregada: {titulo} - {artista}")
                    else:
                        print(f"Error al agregar: {titulo}")
                        
                except Exception as e:
                    print(f"Error procesando archivo {archivo}: {str(e)}")
            
            self.actualizar_combo_canciones()
        
    def actualizar_combo_canciones(self):
        try:
            canciones = self.manejo_principal.obtenerListaCanciones()
            print(f"Canciones obtenidas: {canciones}")  # Depuración
            
            if not canciones:
                print("No hay canciones para mostrar")  # Depuración
                self.combo_canciones['values'] = []
                return
                
            self.combo_canciones['values'] = canciones
            if canciones:  # Asegurarse de que hay canciones antes de seleccionar
                self.combo_canciones.current(0)
            print("Combobox actualizado correctamente")  # Depuración
        except Exception as e:
            print(f"Error al actualizar combobox: {str(e)}")  # Depuración
            
    def seleccionar_cancion(self, event=None):
        seleccion = self.combo_canciones.get()
        if seleccion:
            # Obtener el título de la canción de la selección
            if '. ' in seleccion:
                titulo = seleccion.split('. ', 1)[1]
            else:
                titulo = seleccion
            
            if ' - ' in titulo:
                titulo = titulo.split(' - ')[0].strip()
            
            if self.manejo_principal.reproducir(titulo):
                self.lbl_cancion_actual.config(text=f"Canción actual: {seleccion}")
                self.btn_reproducir.config(text="Pausar")
                self.reproduciendo = True
    
    def reproducir_pausar(self):
        if self.reproduciendo:
            if self.manejo_principal.pausar():
                self.btn_reproducir.config(text="Reproducir")
                self.reproduciendo = False
        else:
            cancion = self.combo_canciones.get()
            if cancion:
                # Extraer el título de la canción seleccionada
                if '. ' in cancion:
                    titulo = cancion.split('. ', 1)[1]
                else:
                    titulo = cancion
                
                if ' - ' in titulo:
                    titulo = titulo.split(' - ')[0].strip()
                
                if self.manejo_principal.reproducir(titulo):
                    self.btn_reproducir.config(text="Pausar")
                    self.reproduciendo = True
    
    def cancion_anterior(self):
        if self.manejo_principal.anterior():
            try:
                # Actualizar interfaz con la canción anterior
                if hasattr(self.manejo_principal.reproductor, 'cancionActual') and self.manejo_principal.reproductor.cancionActual:
                    cancion_info = self.manejo_principal.reproductor.cancionActual.cancion
                    titulo = cancion_info.get('titulo', 'Desconocido')
                    artista = cancion_info.get('artista', 'Desconocido')
                    texto_cancion = f"{titulo} - {artista}"
                    self.lbl_cancion_actual.config(text=f"Canción actual: {texto_cancion}")
                    self.actualizar_combo_seleccion(titulo)
            except AttributeError as e:
                messagebox.showerror("Error", f"No se pudo obtener la información de la canción anterior: {str(e)}")
    
    def verificar_errores(self):
        # Verificar inicialización de pygame
        if not pygame.get_init():
            messagebox.showerror("Error", "Pygame no se inicializó correctamente")
            return False
        
        # Verificar mixer
        if not pygame.mixer.get_init():
            messagebox.showerror("Error", "El mixer de audio no se inicializó")
            return False
    
        return True

    def cancion_siguiente(self):
        if self.manejo_principal.siguiente():
            try:
                # Actualizar interfaz con la canción siguiente
                if hasattr(self.manejo_principal.reproductor, 'cancionActual') and self.manejo_principal.reproductor.cancionActual:
                    cancion_info = self.manejo_principal.reproductor.cancionActual.cancion
                    titulo = cancion_info.get('titulo', 'Desconocido')
                    artista = cancion_info.get('artista', 'Desconocido')
                    texto_cancion = f"{titulo} - {artista}"
                    self.lbl_cancion_actual.config(text=f"Canción actual: {texto_cancion}")
                    self.actualizar_combo_seleccion(titulo)
            except AttributeError as e:
                messagebox.showerror("Error", f"No se pudo obtener la información de la canción siguiente: {str(e)}")
    
    def actualizar_combo_seleccion(self, titulo_cancion):
        valores = self.combo_canciones['values']
        if not valores:
            return
            
        # Buscar la entrada que contiene el título de la canción
        for i, valor in enumerate(valores):
            if titulo_cancion in valor:
                self.combo_canciones.current(i)
                return
    
    def crear_playlist(self):
        seleccion = self.combo_canciones.get()
        if seleccion:
            # Extraer el título de la canción
            if '. ' in seleccion:
                titulo = seleccion.split('. ', 1)[1]
            else:
                titulo = seleccion
                
            if ' - ' in titulo:
                titulo = titulo.split(' - ')[0].strip()
                
            resultado = self.manejo_principal.agregarCancionAPlaylist(titulo)
            if resultado:
                # Agregar a la lista visual
                self.listbox_playlist.insert(tk.END, seleccion)
                messagebox.showinfo("Playlist", f"Se agregó '{seleccion}' a la playlist")
            else:
                messagebox.showerror("Error", "No se pudo agregar la canción a la playlist")
    
    def borrar_cancion_playlist(self):
        seleccion = self.listbox_playlist.curselection()
        if seleccion:
            indice = seleccion[0]
            texto_cancion = self.listbox_playlist.get(indice)
            
            # Extraer el título de la canción
            if '. ' in texto_cancion:
                titulo = texto_cancion.split('. ', 1)[1]
            else:
                titulo = texto_cancion
                
            if ' - ' in titulo:
                titulo = titulo.split(' - ')[0].strip()
                
            resultado = self.manejo_principal.eliminarCancionDePlaylist(titulo)
            if resultado:
                self.listbox_playlist.delete(indice)
                messagebox.showinfo("Playlist", f"Se eliminó '{texto_cancion}' de la playlist")
            else:
                messagebox.showerror("Error", "No se pudo eliminar la canción de la playlist")
    
    def borrar_playlist(self):
        if messagebox.askyesno("Confirmar", "¿Borrar toda la playlist?"):
            self.listbox_playlist.delete(0, tk.END)
            self.manejo_principal.playlistActual = linkedListPlaylist()
            messagebox.showinfo("Playlist", "Se ha borrado la playlist")

    def mostrar_formulario_agregar(self):
        formulario = tk.Toplevel(self.root)
        formulario.title("Agregar Canción")
        formulario.geometry("400x250")
        formulario.resizable(False, False)
        
        # Variable para controlar el estado
        self.formulario_activo = True
        
        def cerrar_formulario():
            self.formulario_activo = False
            formulario.destroy()
        
        formulario.protocol("WM_DELETE_WINDOW", cerrar_formulario)
        
        # Campos del formulario
        tk.Label(formulario, text="Nombre de la canción:").pack(pady=(10, 0))
        entry_nombre = tk.Entry(formulario, width=40)
        entry_nombre.pack()
        
        tk.Label(formulario, text="Artista:").pack(pady=(10, 0))
        entry_artista = tk.Entry(formulario, width=40)
        entry_artista.pack()
        
        # Frame para ruta del archivo
        tk.Label(formulario, text="Ruta del archivo:").pack(pady=(10, 0))
        frame_ruta = tk.Frame(formulario)
        frame_ruta.pack()
        
        entry_ruta = tk.Entry(frame_ruta, width=30)
        entry_ruta.pack(side=tk.LEFT)
        
        def seleccionar_archivo():
            archivo = filedialog.askopenfilename(
                filetypes=(("Archivos MP3", "*.mp3"), ("Archivos WAV", "*.wav"), ("Todos los archivos", "*.*"))
            )
            if archivo:
                entry_ruta.delete(0, tk.END)
                entry_ruta.insert(0, archivo)
        
        btn_buscar = tk.Button(frame_ruta, text="Buscar...", command=seleccionar_archivo)
        btn_buscar.pack(side=tk.LEFT, padx=5)
        
        # Botón para agregar
        def agregar_cancion():
            nombre = entry_nombre.get().strip()
            artista = entry_artista.get().strip()
            ruta = entry_ruta.get().strip()
            
            if not nombre or not ruta:
                messagebox.showerror("Error", "Nombre y ruta del archivo son obligatorios")
                return
            
            try:
                # Verificar si el archivo existe
                if not os.path.exists(ruta):
                    messagebox.showerror("Error", f"El archivo no existe:\n{ruta}")
                    return
                
                # Intentar agregar la canción
                if self.manejo_principal.agregarCancion(nombre, artista, "0:00", ruta):
                    messagebox.showinfo("Éxito", "Canción agregada correctamente")
                    self.actualizar_combo_canciones()
                    cerrar_formulario()
                else:
                    messagebox.showerror("Error", "No se pudo agregar la canción")
            
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error:\n{str(e)}")
        
        btn_agregar = tk.Button(
            formulario, 
            text="Agregar Canción", 
            command=agregar_cancion,
            bg="#4CAF50", 
            fg="white"
        )
        btn_agregar.pack(pady=10)
        
        # Botón cancelar
        btn_cancelar = tk.Button(
            formulario,
            text="Cancelar",
            command=cerrar_formulario,
            bg="#F44336",
            fg="white"
        )
        btn_cancelar.pack(pady=5)
        
        # Centrar formulario
        formulario.transient(self.root)
        formulario.grab_set()
        self.root.wait_window(formulario)

if __name__ == "__main__":
    root = tk.Tk()
    app = ReproductorMusica(root)
    root.mainloop()