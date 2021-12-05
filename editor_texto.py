import tkinter as tk
from tkinter.filedialog import askopenfile, asksaveasfilename

class Editor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Franco Barales - Editor de Texto')
        # Configuracion tamaño minimo de la ventana
        self.rowconfigure(0, minsize=600, weight=1)
        # Configuracion minima de la segunda columna
        self.columnconfigure(1, minsize=600, weight=1)
        # Atributo de campo de texto
        self.campo_texto = tk.Text(self, wrap=tk.WORD) # Para mostrar palabras enteras
        # Atributo de archivo
        self.archivo = None
        # Atributo para saber si ya se abrio un archivo anteriormente
        self.archivo_abierto = False
        # Creacion de componentes
        self._crear_componentes()
        # Crear menu
        self._crear_menu()

    def _crear_componentes(self):
        frame_botones = tk.Frame(self, relief=tk.RAISED, bd=2) # Relieve del marco
        boton_abrir = tk.Button(frame_botones, text='Abrir', command=self._abrir_archivo)
        boton_guardar = tk.Button(frame_botones, text='Guardar', command=self._guardar)
        boton_guardar_como = tk.Button(frame_botones, text='Guardar Como...', command=self._guardar_como)
        # Los botones los expandimos de manera horizontal (sticky = 'we')
        boton_abrir.grid(row=0, column=0, sticky='we', padx=5, pady=5)
        boton_guardar.grid(row=1, column=0, sticky='we', padx=5, pady=5)
        boton_guardar_como.grid(row=2, column=0, sticky='we', padx=5, pady=5)
        # Coloco el frame de manera vertical
        frame_botones.grid(row=0, column=0, sticky='ns')
        # Agregamos el campo de texto
        self.campo_texto.grid(row=0, column=1, sticky='nswe')

    def _crear_menu(self):
        # Creamos el menu de la app
        menu_app = tk.Menu(self)
        self.config(menu=menu_app)
        # Agregamos las opciones a nuestro menu
        # Agregamos menu archivo
        menu_archivo = tk.Menu(menu_app, tearoff=False)
        menu_app.add_cascade(label='Archivo', menu=menu_archivo)
        # Agregamos las opciones del menu de archivo
        menu_archivo.add_command(label='Abrir', command=self._abrir_archivo)
        menu_archivo.add_command(label='Guardar', command=self._guardar)
        menu_archivo.add_command(label='Guardar Como...', command=self._guardar_como)
        menu_archivo.add_command(label='Salir', command=self.quit)

    def _abrir_archivo(self):
        # Abrimos el archivo para edicion (lectura-escritura)
        self.archivo_abierto = askopenfile(mode='r+')
        # Eliminamos el texto anterior
        self.campo_texto.delete(1.0, tk.END)
        # Revisamos si hay un archivo
        if not self.archivo_abierto:
            return
        # Abrimos el archivo en modo lectura/escritura como un recurso
        with open(self.archivo_abierto.name, 'r+') as self.archivo:
            # Leemos el contenido del archivo
            texto = self.archivo.read()
            # Insertamos el contenido del archivo
            self.campo_texto.insert(1.0, texto)
            # Modificamos el titulo de la aplicacion
            self.title(f'*Editor Texto - {self.archivo.name}')


    def _guardar(self):
        # Si ya se abrio previamente un archivo, lo sobreescribimos
        if self.archivo_abierto:
            # Guardamos el archivo (lo abrimos en modo escritura)
            with open(self.archivo_abierto.name, 'w') as self.archivo:
                # Leemos el contenido de la caja de texto
                texto = self.campo_texto.get(1.0, tk.END)
                # Escribimos el contenido al mismo archivo
                self.archivo.write(texto)
                # Cambiamos el nombre del titulo de la app
                self.title(f'Editor Texto - {self.archivo.name}')
        else:
            self._guardar_como()

    def _guardar_como(self):
        # Salvamos el archivo actual como un nuevo archivo
        self.archivo = asksaveasfilename(
            defaultextension='txt',
            filetypes=[('Archivos de Texto', '*.txt'), ('Todos los archivos', '*.*')]
        )
        if not self.archivo:
            return
        # Abrimos el archivo en modo escritura (write)
        with open(self.archivo, 'w') as archivo:
            # Leemos el contenido de la caja de texto
            texto = self.campo_texto.get(1.0, tk.END)
            # Escribimos el contenido al nuevo archivo
            self.archivo.write(texto)
            # Cambiamos el nombre del archivo
            self.title(f'Editor Texto - {self.archivo}')
            # Indicamos que hemos abierto un archivo
            self.archivo_abierto = archivo


if __name__ == '__main__':
    editor = Editor()
    editor.mainloop()