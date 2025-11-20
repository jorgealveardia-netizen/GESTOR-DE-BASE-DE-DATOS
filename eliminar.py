from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
KEY = 'C:/Users/Pc/Desktop/GESTOR DE BASE DE DATOS/key.json'
SPREADSHEET_ID = '163VoE5a1F1GxG7T-JPMTpOwNFJPbB1JSbjZ0rkGLNWM'


creds = service_account.Credentials.from_service_account_file(KEY, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()


try:
    spreadsheet_metadata = sheet.get(spreadsheetId=SPREADSHEET_ID).execute()
    
    hoja_id = next(
        (s['properties']['sheetId'] 
         for s in spreadsheet_metadata.get('sheets', []) 
         if s['properties']['title'] == 'Hoja 1'),
        None
    )
    
    if hoja_id is None:
        raise ValueError("No se encontró la hoja con el título 'Hoja 1'.")

except Exception as e:
    print(f" Error al obtener el ID de la hoja: {e}")
    exit()


fila_a_eliminar_str = input(" Introduce el NÚMERO DE FILA completo a eliminar (ej: 4 para borrar a Emmanuel): ")

try:
    fila_a_eliminar = int(fila_a_eliminar_str)
except ValueError:
    print(" Por favor, introduce un número de fila válido.")
    exit()


start_index = fila_a_eliminar - 1
end_index = fila_a_eliminar 


requests = [{
    'deleteDimension': {
        'range': {
            'sheetId': hoja_id,
            'dimension': 'ROWS',  
            'startIndex': start_index,
            'endIndex': end_index
        }
    }
}]


try:
    result = sheet.batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body={'requests': requests}
    ).execute()

    print(f" Fila {fila_a_eliminar} eliminada correctamente.")
    print("Las filas inferiores han subido para llenar el espacio.")

except Exception as e:
    print(f" Error al ejecutar la eliminación de la fila: {e}")