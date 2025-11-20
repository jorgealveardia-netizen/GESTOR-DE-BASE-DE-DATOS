from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
KEY = 'C:/Users/Pc/Desktop/GESTOR DE BASE DE DATOS/key.json'
SPREADSHEET_ID = '163VoE5a1F1GxG7T-JPMTpOwNFJPbB1JSbjZ0rkGLNWM'


creds = service_account.Credentials.from_service_account_file(KEY, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()


nuevo_valor = input(" Introduce el DATO o VALOR que deseas escribir: ")

if not nuevo_valor:
    print(" Operación cancelada: No se introdujo ningún valor.")
    exit()


columna = input("Introduce la COLUMNA (ej: A, B, C): ").upper()
fila_str = input(" Introduce la FILA (ej: 5, 6, 7): ")

try:
    fila = int(fila_str)
except ValueError:
    print(" Por favor, introduce un número de fila válido.")
    exit()


RANGO_A_ESCRIBIR = f'Hoja 1!{columna}{fila}'


values = [[nuevo_valor]] 


try:
    result = sheet.values().update(spreadsheetId=SPREADSHEET_ID,
                                  range=RANGO_A_ESCRIBIR,
                                  valueInputOption='USER_ENTERED',
                                  body={'values': values}).execute()

    print(f"\n Dato escrito correctamente.")
    print(f"   - Celda objetivo: {RANGO_A_ESCRIBIR}")
    print(f"   - Valor escrito: {nuevo_valor}")
    print(f"   - Celdas modificadas: {result.get('updatedCells')}")
except Exception as e:
    print(f" Error al escribir los datos: {e}")