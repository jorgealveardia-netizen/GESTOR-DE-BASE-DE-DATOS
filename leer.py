from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
KEY = 'C:/Users/Pc/Desktop/GESTOR DE BASE DE DATOS/key.json'
SPREADSHEET_ID = '163VoE5a1F1GxG7T-JPMTpOwNFJPbB1JSbjZ0rkGLNWM'

creds = None
creds = service_account.Credentials.from_service_account_file(KEY, scopes=SCOPES)

service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

# Llamada a la api
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range='Hoja 1!A1:A17').execute()
# Extraemos values del resultado
values = result.get('values', [])

if not values:
    print("No se encontraron datos en el rango especificado.")
else:
    print("\n--- Lista de NOMBRES ---")
    
    # El primer valor es el encabezado, lo separamos
    encabezado = values[0][0]
    datos_lista = values[1:]
    
    print(f"Encabezado: {encabezado}\n")
    
    # Iteramos sobre los datos y los mostramos bonitos
    for i, fila in enumerate(datos_lista):
        # La fila es una lista (ej: ['JORGE']), por eso usamos fila[0]
        nombre = fila[0] if fila else "Celda vacía"
        print(f"[{i + 1}] {nombre}")

    print("--------------------------")