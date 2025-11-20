import tkinter as tk
from tkinter import ttk, messagebox
from google.oauth2 import service_account
from googleapiclient.discovery import build

# --- CONFIGURACIÓN DE GOOGLE SHEETS ---
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
# !!! ATENCIÓN: Cambia esta ruta a la ubicación correcta de tu 'key.json' !!!
KEY = 'C:/Users/Pc/Desktop/GESTOR DE BASE DE DATOS/key.json' 
SPREADSHEET_ID = '163VoE5a1F1GxG7T-JPMTpOwNFJPbB1JSbjZ0rkGLNWM' 


# --- CONEXIÓN Y SERVICIO ---
def get_sheets_service():
    """Inicializa y retorna el objeto de servicio de Google Sheets."""
    try:
        creds = service_account.Credentials.from_service_account_file(KEY, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=creds)
        return service.spreadsheets()
    except Exception as e:
        messagebox.showerror("Error de Conexión", f"No se pudo conectar con Google Sheets:\n{e}")
        return None

sheet = get_sheets_service()


# --- FUNCIONES DE OPERACIÓN ---

# 5. Función de REFRESCAR LA PESTAÑA DE LECTURA (¡Necesaria para el auto-refresco!)
def refrescar_visor_datos(app_instance):
    """Llama a la función leer_datos con el treeview de la aplicación."""
    # El Treeview debe existir y estar configurado
    if hasattr(app_instance, 'tree'):
        # show_message=False previene el pop-up de éxito en cada actualización automática
        leer_datos(app_instance.tree, show_message=False)


# 1. Función de LECTURA (MODIFICADA para mostrar letras/números de filas/columnas)
def leer_datos(treeview, show_message=True):
    if not sheet: return
    try:
        # Rango actualizado para incluir las columnas A, B y C
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range='Hoja 1!A1:C17').execute()
        values = result.get('values', [])
        
        # Limpiar Treeview (columnas y datos)
        treeview.delete(*treeview.get_children())
        # Eliminamos la línea treeview["columns"] = () aquí, ya que la reconfiguraremos más abajo
        # Eliminamos la línea treeview["show"] = "headings" aquí, ya que la cambiaremos más abajo

        if not values:
            if show_message:
                messagebox.showinfo("Información", "No se encontraron datos en el rango especificado.")
            return

        encabezado = values[0]
        datos_lista = values[1:]
        
        # --- Configurar las columnas del Treeview con el encabezado ---
        
        # 💡 CAMBIO CLAVE 1: Configura 'show' para incluir la columna 'tree' (#0) y los encabezados.
        # 'tree' se refiere a la columna #0 (la primera, que usaremos para el número de fila).
        treeview["show"] = "tree headings"
        
        # Generamos los IDs de las columnas de datos (0, 1, 2, ...)
        column_ids = [str(i) for i in range(len(encabezado))]
        treeview["columns"] = tuple(column_ids) 
        
        # 💡 CAMBIO CLAVE 2: Asignamos el texto y ancho a la columna #0 (la de las filas).
        treeview.heading("#0", text="Fila", anchor="center")
        treeview.column("#0", width=40, anchor="center", stretch=tk.NO) # stretch=tk.NO previene que se estire
        
        # Configurar las columnas de datos (las de Google Sheets)
        for i, col_name in enumerate(encabezado):
            # Asignamos la letra de la columna de Excel (A, B, C...)
            # chr(65 + i) convierte 0 -> 'A', 1 -> 'B', etc.
            nombre_columna_excel = chr(65 + i)
            
            # 💡 CAMBIO CLAVE 3: El encabezado ahora tiene la letra de Excel + nombre de columna.
            treeview.heading(str(i), text=f"{nombre_columna_excel} - {col_name}", anchor="center")
            treeview.column(str(i), width=120, anchor="w") 

        # --- Insertar datos ---
        for i, fila in enumerate(datos_lista):
            # i+2 es el número real de la fila en Google Sheets (empieza en 2)
            fila_real = str(i + 2) 
            # Insertamos el número de fila en la columna especial 'text' (columna #0)
            treeview.insert("", "end", text=fila_real, values=fila)
        
        # Mensaje solo si es una llamada manual (show_message=True)
        if show_message:
            messagebox.showinfo("Éxito", "Datos leídos y actualizados correctamente.")

    except Exception as e:
        messagebox.showerror("Error", f"Error al leer los datos:\n{e}")

# 2. Función de ESCRITURA (MODIFICADA: pasa app_instance y refresca)
def escribir_datos(entry_valor, entry_columna, entry_fila, app_instance):
    if not sheet: return

    nuevo_valor = entry_valor.get().strip()
    columna = entry_columna.get().strip().upper()
    fila_str = entry_fila.get().strip()

    if not nuevo_valor or not columna or not fila_str:
        messagebox.showwarning("Advertencia", "Todos los campos (Valor, Columna, Fila) son obligatorios.")
        return

    try:
        fila = int(fila_str)
        if fila <= 0: raise ValueError
    except ValueError:
        messagebox.showerror("Error de Entrada", "Por favor, introduce un número de fila válido y positivo.")
        return
        
    RANGO_A_ESCRIBIR = f'Hoja 1!{columna}{fila}'
    values = [[nuevo_valor]] 

    try:
        sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=RANGO_A_ESCRIBIR,
                              valueInputOption='USER_ENTERED', body={'values': values}).execute()
                                      
        messagebox.showinfo("Éxito", f"Dato escrito correctamente en {RANGO_A_ESCRIBIR}.")
        refrescar_visor_datos(app_instance) # Refresco automático
        
        entry_valor.delete(0, tk.END)
        entry_columna.delete(0, tk.END)
        entry_fila.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Error", f"Error al escribir los datos:\n{e}")

# 3. Función de MODIFICAR (MODIFICADA: pasa app_instance y refresca)
def modificar_datos(entry_fila_mod, entry_columna_mod, entry_nuevo_valor, app_instance):
    if not sheet: return

    fila_a_modificar_str = entry_fila_mod.get().strip()
    columna_a_modificar = entry_columna_mod.get().strip().upper()
    nuevo_valor = entry_nuevo_valor.get().strip()

    if not fila_a_modificar_str or not columna_a_modificar or not nuevo_valor:
        messagebox.showwarning("Advertencia", "Debes especificar la Columna, Fila y el Nuevo Valor.")
        return
    try:
        fila_a_modificar = int(fila_a_modificar_str)
        if fila_a_modificar <= 0: raise ValueError
    except ValueError:
        messagebox.showerror("Error de Entrada", "Por favor, introduce un número de fila válido y positivo.")
        return
        
    RANGO_A_ACTUALIZAR = f'Hoja 1!{columna_a_modificar}{fila_a_modificar}'
    values = [[nuevo_valor]] 

    try:
        sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=RANGO_A_ACTUALIZAR,
                              valueInputOption='USER_ENTERED', body={'values': values}).execute()

        messagebox.showinfo("Éxito", f"Dato modificado correctamente.\nCelda actualizada: {RANGO_A_ACTUALIZAR}")
        refrescar_visor_datos(app_instance) # Refresco automático
        
        entry_fila_mod.delete(0, tk.END)
        entry_columna_mod.delete(0, tk.END)
        entry_nuevo_valor.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Error", f"Error al modificar los datos:\n{e}")


# 4. Función de BORRAR CONTENIDO DE CELDAS (MODIFICADA: pasa app_instance y refresca)
def borrar_celdas(entry_rango_del, app_instance):
    if not sheet: return

    rango_a_borrar = entry_rango_del.get().strip().upper()

    if not rango_a_borrar:
        messagebox.showwarning("Advertencia", "Debes introducir el rango de celdas a borrar (ej: A5 o A5:C5).")
        return
        
    try:
        sheet.values().clear(spreadsheetId=SPREADSHEET_ID, range=f'Hoja 1!{rango_a_borrar}', body={}).execute()

        messagebox.showinfo("Éxito", f"Contenido de la(s) celda(s) borrado correctamente.\nRango afectado: {rango_a_borrar}")
        refrescar_visor_datos(app_instance) # Refresco automático
        entry_rango_del.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Error", f"Error al borrar el contenido de la(s) celda(s):\n{e}")


# --- CONFIGURACIÓN DE LA INTERFAZ ---
class GestorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestor de Base de Datos Google Sheets")
        self.geometry("650x700") # Aumentamos el tamaño para la tabla
        
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10, padx=10, expand=True, fill="both")
        
        # 1. CREAMOS EL TREEVIEW UNA SOLA VEZ (y lo hacemos atributo de la clase)
        # Aquí eliminamos 'show="headings"' para que el control lo tome leer_datos
        self.tree = ttk.Treeview(self, columns=("0",), show="") 
        
        # 2. CONFIGURAMOS EL NAVEGADOR
        self.crear_pestana_leer()
        self.crear_pestana_escribir()
        self.crear_pestana_modificar()
        self.crear_pestana_eliminar()
        
        # Este evento se dispara cuando se cambia de pestaña
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)
        
    def on_tab_change(self, event):
        """Maneja el evento de cambio de pestaña para asegurar que el Treeview se muestre."""
        # Desempacamos el Treeview (si estaba empacado en otra pestaña)
        self.tree.pack_forget() 
        
        # Obtenemos la pestaña actualmente seleccionada
        selected_tab_id = self.notebook.select()
        selected_tab = self.notebook.nametowidget(selected_tab_id)
        
        # Si la pestaña seleccionada es alguna de las pestañas que debe mostrar el Treeview
        if selected_tab in [self.frame_escribir, self.frame_modificar, self.frame_eliminar, self.frame_leer]:
            # El Treeview se reasigna a su nuevo contenedor y se empaca
            self.tree.master = selected_tab
            self.tree.pack(fill="both", expand=True, side=tk.BOTTOM, pady=10, padx=10)
            # Aseguramos que los datos estén frescos
            refrescar_visor_datos(self)


    # --- Pestaña: LEER (Ver Datos) ---
    def crear_pestana_leer(self):
        self.frame_leer = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.frame_leer, text="🔍 Ver Datos")

        # ❗ LÍNEAS COMENTADAS: Estas configuraciones de #0 ahora están en leer_datos
        # self.tree.heading("#0", text="Fila", anchor="center")
        # self.tree.column("#0", width=40, anchor="center") 
        
        self.tree.master = self.frame_leer # Asignamos el Treeview al frame
        self.tree.pack(fill="both", expand=True)
        
        # Botón para actualizar los datos (Llamada manual con mensaje de éxito)
        btn_leer = ttk.Button(self.frame_leer, text="Actualizar Datos de Google Sheets", 
                              command=lambda: leer_datos(self.tree, show_message=True))
        btn_leer.pack(pady=10)
        
        # Cargar los datos al iniciar la pestaña
        leer_datos(self.tree, show_message=False)
        
    # --- Pestaña: ESCRIBIR (INTEGRADA) ---
    def crear_pestana_escribir(self):
        self.frame_escribir = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.frame_escribir, text="✏️ Escribir Dato")
        
        # Contenedor de Entradas (parte superior)
        labels_frame = ttk.Frame(self.frame_escribir)
        labels_frame.pack(pady=10, padx=50) # Menos pady para dejar espacio a la tabla

        # Campos de entrada...
        ttk.Label(labels_frame, text="Valor a Escribir:").grid(row=0, column=0, sticky="w", pady=5)
        entry_valor = ttk.Entry(labels_frame, width=30)
        entry_valor.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(labels_frame, text="Columna (Ej: A, B):").grid(row=1, column=0, sticky="w", pady=5)
        entry_columna = ttk.Entry(labels_frame, width=30)
        entry_columna.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(labels_frame, text="Fila (Ej: 5):").grid(row=2, column=0, sticky="w", pady=5)
        entry_fila = ttk.Entry(labels_frame, width=30)
        entry_fila.grid(row=2, column=1, padx=10, pady=5)
        
        # Botón - PASAR 'self'
        btn_escribir = ttk.Button(self.frame_escribir, text="Escribir Dato en Celda", 
                                  command=lambda: escribir_datos(entry_valor, entry_columna, entry_fila, self))
        btn_escribir.pack(pady=10)
        
        ttk.Separator(self.frame_escribir, orient='horizontal').pack(fill='x', pady=5)
        ttk.Label(self.frame_escribir, text="Vista de Datos Actualizados:").pack(pady=5)
        
        # **NO EMPACAMOS EL TREEVIEW AQUÍ. Se empacará al hacer clic en la pestaña con on_tab_change.**

        
    # --- Pestaña: MODIFICAR (INTEGRADA) ---
    def crear_pestana_modificar(self):
        self.frame_modificar = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.frame_modificar, text="📝 Modificar Celda") 
        
        # Contenedor de Entradas (parte superior)
        labels_frame = ttk.Frame(self.frame_modificar)
        labels_frame.pack(pady=10, padx=50)

        # Campos de entrada...
        ttk.Label(labels_frame, text="Número de Fila:").grid(row=0, column=0, sticky="w", pady=5)
        entry_fila_mod = ttk.Entry(labels_frame, width=30)
        entry_fila_mod.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(labels_frame, text="Columna (Ej: A, B):").grid(row=1, column=0, sticky="w", pady=5)
        entry_columna_mod = ttk.Entry(labels_frame, width=30)
        entry_columna_mod.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(labels_frame, text="Nuevo Valor:").grid(row=2, column=0, sticky="w", pady=5) 
        entry_nuevo_valor = ttk.Entry(labels_frame, width=30)
        entry_nuevo_valor.grid(row=2, column=1, padx=10, pady=5)

        # Botón - PASAR 'self'
        btn_modificar = ttk.Button(self.frame_modificar, text="Modificar Celda", 
                                  command=lambda: modificar_datos(entry_fila_mod, entry_columna_mod, entry_nuevo_valor, self))
        btn_modificar.pack(pady=10)
        
        ttk.Separator(self.frame_modificar, orient='horizontal').pack(fill='x', pady=5)
        ttk.Label(self.frame_modificar, text="Vista de Datos Actualizados:").pack(pady=5)

    # --- Pestaña: ELIMINAR (INTEGRADA) ---
    def crear_pestana_eliminar(self):
        self.frame_eliminar = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.frame_eliminar, text="🗑️ Borrar Contenido") 
        
        # Contenedor de Entradas (parte superior)
        labels_frame = ttk.Frame(self.frame_eliminar)
        labels_frame.pack(pady=10, padx=50)

        # Campos de entrada...
        ttk.Label(labels_frame, text="Rango a Borrar (Ej: A5 o A5:C5):").grid(row=0, column=0, sticky="w", pady=5)
        entry_rango_del = ttk.Entry(labels_frame, width=30)
        entry_rango_del.grid(row=0, column=1, padx=10, pady=5)
        
        # Botón - PASAR 'self'
        btn_eliminar = ttk.Button(self.frame_eliminar, text="Borrar Contenido de Celda(s)", 
                                  command=lambda: borrar_celdas(entry_rango_del, self))
        btn_eliminar.pack(pady=10)
        
        ttk.Label(self.frame_eliminar, text="✅ Esta acción elimina el valor de la(s) celda(s), sin eliminar la fila.", foreground="green").pack(pady=5)
        
        ttk.Separator(self.frame_eliminar, orient='horizontal').pack(fill='x', pady=5)
        ttk.Label(self.frame_eliminar, text="Vista de Datos Actualizados:").pack(pady=5)


if __name__ == "__main__":
    if sheet: 
        app = GestorApp()
        app.mainloop()
    else:
        print("\nEl gestor no se pudo iniciar debido a un error de conexión. Revisa la ruta de tu KEY.")