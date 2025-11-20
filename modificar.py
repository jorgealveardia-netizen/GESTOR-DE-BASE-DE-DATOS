from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
KEY = 'C:/Users/Pc/Desktop/GESTOR DE BASE DE DATOS/key.json'
SPREADSHEET_ID = '163VoE5a1F1GxG7T-JPMTpOwNFJPbB1JSbjZ0rkGLNWM'


creds = service_account.Credentials.from_service_account_file(KEY, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()


try:
    fila_a_modificar_str = input(" Introduce el NÚMERO DE FILA que deseas modificar (ej: 3 para Valentina): ")
    fila_a_modificar = int(fila_a_modificar_str)
except ValueError:
    print(" Por favor, introduce un número de fila válido.")
    exit()


nuevo_valor = input(f" Introduce el NUEVO VALOR para la Fila {fila_a_modificar} (Columna A): ")

if not nuevo_valor:
    print(" Operación cancelada: No se introdujo un nuevo valor.")
    exit()


RANGO_A_ACTUALIZAR = f'Hoja 1!A{fila_a_modificar}'

values = [[nuevo_valor]] 


try:
    result = sheet.values().update(spreadsheetId=SPREADSHEET_ID,
                                  range=RANGO_A_ACTUALIZAR,
                                  valueInputOption='USER_ENTERED',
                                  body={'values': values}).execute()

    print(f"\n Dato modificado correctamente.")
    print(f"   - Celda actualizada: {RANGO_A_ACTUALIZAR}")
    print(f"   - Nuevo valor: {nuevo_valor}")
    print(f"   - Celdas modificadas: {result.get('updatedCells')}")
except Exception as e:
    print(f" Error al modificar los datos: {e}")