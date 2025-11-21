import tkinter as tk
from tkinter import ttk, messagebox
from google.oauth2 import service_account
from googleapiclient.discovery import build
import sys # Importar sys para salir en caso de error crítico

# --- CONFIGURACIÓN DE GOOGLE SHEETS ---
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
# !!! ATENCIÓN: Confirma esta ruta, si está en el mismo folder, usa 'key.json' !!!
KEY = 'C:/Users/Estudiantes/Desktop/Gestor de agendamiento de citas medicas/key.json'  
SPREADSHEET_ID = '163VoE5a1F1GxG7T-JPMTpOwNFJPbB1JSbjZ0rkGLNWM' 
HOJA_NOMBRE = 'Hoja 1'

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

# 7. Función de REFRESCAR LA PESTAÑA DE LECTURA (¡Necesaria para el auto-refresco!)
def refrescar_visor_datos(app_instance):
    """Llama a la función leer_datos con el treeview de la aplicación."""
    if hasattr(app_instance, 'tree'):
        # show_message=False previene el pop-up de éxito en cada actualización automática
        leer_datos(app_instance.tree, show_message=False)


# 1. Función de LECTURA (MODIFICADA para leer hasta la columna D)
def leer_datos(treeview, show_message=True):
    if not sheet: return
    try:
        # RANGO MODIFICADO: Ahora lee hasta la columna D (FECHA DE CITA)
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=f'{HOJA_NOMBRE}!A1:D17').execute()
        values = result.get('values', [])
        
        # Limpiar Treeview (columnas y datos)
        treeview.delete(*treeview.get_children())

        if not values:
            if show_message:
                messagebox.showinfo("Información", "No se encontraron datos en el rango especificado.")
            return

        encabezado = values[0]
        datos_lista = values[1:]
        
        # --- Configurar las columnas del Treeview con el encabezado ---
        
        treeview["show"] = "tree headings"
        column_ids = [str(i) for i in range(len(encabezado))]
        treeview["columns"] = tuple(column_ids) 
        
        # Columna de Fila
        treeview.heading("#0", text="Fila", anchor="center")
        treeview.column("#0", width=40, anchor="center", stretch=tk.NO)
        
        # Configurar las columnas de datos (las de Google Sheets)
        for i, col_name in enumerate(encabezado):
            nombre_columna_excel = chr(65 + i)
            
            # Ajustar ancho para las columnas de datos
            ancho_columna = 120 
            if col_name.upper().startswith('FECHA'):
                ancho_columna = 150 
            
            treeview.heading(str(i), text=f"{nombre_columna_excel} - {col_name}", anchor="center")
            treeview.column(str(i), width=ancho_columna, anchor="w") 

        # --- Insertar datos ---
        for i, fila in enumerate(datos_lista):
            fila_real = str(i + 2) 
            treeview.insert("", "end", text=fila_real, values=fila)
        
        if show_message:
            messagebox.showinfo("Éxito", "Datos leídos y actualizados correctamente.")

    except Exception as e:
        messagebox.showerror("Error", f"Error al leer los datos:\n{e}")

# 2. NUEVA Función para AGENDAR CITA (Escribir una fila completa)
def agendar_cita(entry_nombres, entry_apellidos, entry_eps, entry_fecha, app_instance):
    if not sheet: return

    nombres = entry_nombres.get().strip()
    apellidos = entry_apellidos.get().strip()
    eps = entry_eps.get().strip()
    fecha = entry_fecha.get().strip()

    if not all([nombres, apellidos, eps, fecha]):
        messagebox.showwarning("Advertencia", "Todos los campos de la cita (Nombres, Apellidos, EPS, Fecha) son obligatorios.")
        return
        
    # El orden debe coincidir con el orden de las columnas en Google Sheets: A, B, C, D
    nueva_fila = [nombres, apellidos, eps, fecha]
    
    try:
        # Añade la nueva fila al final de la hoja.
        sheet.values().append(spreadsheetId=SPREADSHEET_ID, 
                              range=f'{HOJA_NOMBRE}!A1', # Rango de inicio
                              valueInputOption='USER_ENTERED', 
                              body={'values': [nueva_fila]}).execute()
                                      
        messagebox.showinfo("Éxito", f"Cita para {nombres} {apellidos} agendada correctamente.")
        
        # Limpiar entradas
        entry_nombres.delete(0, tk.END)
        entry_apellidos.delete(0, tk.END)
        entry_eps.delete(0, tk.END)
        entry_fecha.delete(0, tk.END)
        
        refrescar_visor_datos(app_instance) # Refresco automático

    except Exception as e:
        messagebox.showerror("Error", f"Error al agendar la cita:\n{e}")


# 3. Función de ESCRITURA (Original: para escribir un único dato, columna y fila)
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
        
    RANGO_A_ESCRIBIR = f'{HOJA_NOMBRE}!{columna}{fila}'
    values = [[nuevo_valor]] 

    try:
        sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=RANGO_A_ESCRIBIR,
                              valueInputOption='USER_ENTERED', body={'values': values}).execute()
                                      
        messagebox.showinfo("Éxito", f"Dato escrito correctamente en {RANGO_A_ESCRIBIR}.")
        refrescar_visor_datos(app_instance)
        
        entry_valor.delete(0, tk.END)
        entry_columna.delete(0, tk.END)
        entry_fila.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Error", f"Error al escribir los datos:\n{e}")

# 4. Función de MODIFICAR (Original: modificar una única celda)
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
        
    RANGO_A_ACTUALIZAR = f'{HOJA_NOMBRE}!{columna_a_modificar}{fila_a_modificar}'
    values = [[nuevo_valor]] 

    try:
        sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=RANGO_A_ACTUALIZAR,
                              valueInputOption='USER_ENTERED', body={'values': values}).execute()

        messagebox.showinfo("Éxito", f"Dato modificado correctamente.\nCelda actualizada: {RANGO_A_ACTUALIZAR}")
        refrescar_visor_datos(app_instance) 
        
        entry_fila_mod.delete(0, tk.END)
        entry_columna_mod.delete(0, tk.END)
        entry_nuevo_valor.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Error", f"Error al modificar los datos:\n{e}")


# 5. Función de BORRAR CONTENIDO DE CELDAS (Original: borrar contenido)
def borrar_celdas(entry_rango_del, app_instance):
    if not sheet: return

    rango_a_borrar = entry_rango_del.get().strip().upper()

    if not rango_a_borrar:
        messagebox.showwarning("Advertencia", "Debes introducir el rango de celdas a borrar (ej: A5 o A5:C5).")
        return
        
    try:
        sheet.values().clear(spreadsheetId=SPREADSHEET_ID, range=f'{HOJA_NOMBRE}!{rango_a_borrar}', body={}).execute()

        messagebox.showinfo("Éxito", f"Contenido de la(s) celda(s) borrado correctamente.\nRango afectado: {rango_a_borrar}")
        refrescar_visor_datos(app_instance) 
        entry_rango_del.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Error", f"Error al borrar el contenido de la(s) celda(s):\n{e}")


# --- CONFIGURACIÓN DE LA INTERFAZ ---
class GestorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestor de Agendamiento de Citas Médicas") # Nuevo título
        self.geometry("700x750") 
        
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10, padx=10, expand=True, fill="both")
        
        # 1. CREAMOS EL TREEVIEW UNA SOLA VEZ (y lo hacemos atributo de la clase)
        self.tree = ttk.Treeview(self, columns=("0",), show="") 
        
        # 2. CONFIGURAMOS EL NAVEGADOR
        self.crear_pestana_leer()
        self.crear_pestana_agendar() # NUEVA PESTAÑA PRINCIPAL
        self.crear_pestana_escribir()
        self.crear_pestana_modificar()
        self.crear_pestana_eliminar()
        
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)
        
    def on_tab_change(self, event):
        """Maneja el evento de cambio de pestaña para asegurar que el Treeview se muestre."""
        self.tree.pack_forget() 
        
        selected_tab_id = self.notebook.select()
        selected_tab = self.notebook.nametowidget(selected_tab_id)
        
        # Si la pestaña seleccionada es alguna de las que debe mostrar el Treeview
        if selected_tab in [self.frame_escribir, self.frame_modificar, self.frame_eliminar, self.frame_leer, self.frame_agendar]:
            self.tree.master = selected_tab
            self.tree.pack(fill="both", expand=True, side=tk.BOTTOM, pady=10, padx=10)
            refrescar_visor_datos(self)


    # --- Pestaña: LEER (Ver Datos) ---
    def crear_pestana_leer(self):
        self.frame_leer = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.frame_leer, text="🔍 Ver Datos")
        
        self.tree.master = self.frame_leer 
        self.tree.pack(fill="both", expand=True)
        
        btn_leer = ttk.Button(self.frame_leer, text="Actualizar Datos de Google Sheets", 
                              command=lambda: leer_datos(self.tree, show_message=True))
        btn_leer.pack(pady=10)
        
        leer_datos(self.tree, show_message=False)

    # --- NUEVA Pestaña: AGENDAR CITA (CRUD COMPLETO) ---
    def crear_pestana_agendar(self):
        self.frame_agendar = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.frame_agendar, text="➕ Agendar Cita (CRUD)")

        labels_frame = ttk.Frame(self.frame_agendar)
        labels_frame.pack(pady=10, padx=50) 
        
        # Nombres
        ttk.Label(labels_frame, text="1. Nombres:").grid(row=0, column=0, sticky="w", pady=5)
        entry_nombres = ttk.Entry(labels_frame, width=30)
        entry_nombres.grid(row=0, column=1, padx=10, pady=5)

        # Apellidos
        ttk.Label(labels_frame, text="2. Apellidos:").grid(row=1, column=0, sticky="w", pady=5)
        entry_apellidos = ttk.Entry(labels_frame, width=30)
        entry_apellidos.grid(row=1, column=1, padx=10, pady=5)

        # EPS
        ttk.Label(labels_frame, text="3. EPS:").grid(row=2, column=0, sticky="w", pady=5)
        entry_eps = ttk.Entry(labels_frame, width=30)
        entry_eps.grid(row=2, column=1, padx=10, pady=5)

        # Fecha de Cita
        ttk.Label(labels_frame, text="4. Fecha de Cita (DD/MM/AAAA):").grid(row=3, column=0, sticky="w", pady=5)
        entry_fecha = ttk.Entry(labels_frame, width=30)
        entry_fecha.grid(row=3, column=1, padx=10, pady=5)

        # Botón - Llamar a la función agendar_cita con las 4 entradas
        btn_agendar = ttk.Button(self.frame_agendar, text="CONFIRMAR AGENDAMIENTO (Añadir Fila)", 
                                  command=lambda: agendar_cita(entry_nombres, entry_apellidos, entry_eps, entry_fecha, self))
        btn_agendar.pack(pady=15)
        
        ttk.Separator(self.frame_agendar, orient='horizontal').pack(fill='x', pady=5)
        ttk.Label(self.frame_agendar, text="Vista de Citas Actualizadas:").pack(pady=5)
        
        # El Treeview se empaca con on_tab_change
        
    # --- Pestaña: ESCRIBIR (Original: un solo dato) ---
    def crear_pestana_escribir(self):
        self.frame_escribir = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.frame_escribir, text="✏️ Escribir Dato (Individual)")
        
        labels_frame = ttk.Frame(self.frame_escribir)
        labels_frame.pack(pady=10, padx=50)

        ttk.Label(labels_frame, text="Valor a Escribir:").grid(row=0, column=0, sticky="w", pady=5)
        entry_valor = ttk.Entry(labels_frame, width=30)
        entry_valor.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(labels_frame, text="Columna (Ej: A, B):").grid(row=1, column=0, sticky="w", pady=5)
        entry_columna = ttk.Entry(labels_frame, width=30)
        entry_columna.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(labels_frame, text="Fila (Ej: 5):").grid(row=2, column=0, sticky="w", pady=5)
        entry_fila = ttk.Entry(labels_frame, width=30)
        entry_fila.grid(row=2, column=1, padx=10, pady=5)
        
        btn_escribir = ttk.Button(self.frame_escribir, text="Escribir Dato en Celda", 
                                  command=lambda: escribir_datos(entry_valor, entry_columna, entry_fila, self))
        btn_escribir.pack(pady=10)
        
        ttk.Separator(self.frame_escribir, orient='horizontal').pack(fill='x', pady=5)
        ttk.Label(self.frame_escribir, text="Vista de Datos Actualizados:").pack(pady=5)
        

    # --- Pestaña: MODIFICAR (Original: un solo dato) ---
    def crear_pestana_modificar(self):
        self.frame_modificar = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.frame_modificar, text="📝 Modificar Celda") 
        
        labels_frame = ttk.Frame(self.frame_modificar)
        labels_frame.pack(pady=10, padx=50)

        ttk.Label(labels_frame, text="Número de Fila:").grid(row=0, column=0, sticky="w", pady=5)
        entry_fila_mod = ttk.Entry(labels_frame, width=30)
        entry_fila_mod.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(labels_frame, text="Columna (Ej: A, B):").grid(row=1, column=0, sticky="w", pady=5)
        entry_columna_mod = ttk.Entry(labels_frame, width=30)
        entry_columna_mod.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(labels_frame, text="Nuevo Valor:").grid(row=2, column=0, sticky="w", pady=5) 
        entry_nuevo_valor = ttk.Entry(labels_frame, width=30)
        entry_nuevo_valor.grid(row=2, column=1, padx=10, pady=5)

        btn_modificar = ttk.Button(self.frame_modificar, text="Modificar Celda", 
                                  command=lambda: modificar_datos(entry_fila_mod, entry_columna_mod, entry_nuevo_valor, self))
        btn_modificar.pack(pady=10)
        
        ttk.Separator(self.frame_modificar, orient='horizontal').pack(fill='x', pady=5)
        ttk.Label(self.frame_modificar, text="Vista de Datos Actualizados:").pack(pady=5)

    # --- Pestaña: ELIMINAR (Original: Borrar Contenido) ---
    def crear_pestana_eliminar(self):
        self.frame_eliminar = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.frame_eliminar, text="🗑️ Borrar Contenido") 
        
        labels_frame = ttk.Frame(self.frame_eliminar)
        labels_frame.pack(pady=10, padx=50)

        ttk.Label(labels_frame, text="Rango a Borrar (Ej: A5 o A5:C5):").grid(row=0, column=0, sticky="w", pady=5)
        entry_rango_del = ttk.Entry(labels_frame, width=30)
        entry_rango_del.grid(row=0, column=1, padx=10, pady=5)
        
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
        # Se cierra la aplicación si la conexión inicial falla
        sys.exit(1)