from oauth2client.service_account import ServiceAccountCredentials
import gspread
import pandas as pd

def sheet_a_dataframe(sheet_id,nombre_hoja=None,id_hoja=None):
    if not nombre_hoja and not id_hoja:
        raise Exception('No hay hoja seleccionada')
    # Configura las credenciales
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(r"contabilidad-431214-ff591307d9b0.json", scope)
    client = gspread.authorize(creds)

    # Acceder a la hoja de Google Sheets
    sheet = client.open_by_key(sheet_id)
    # print(sheet.worksheets())

    if nombre_hoja:    
        worksheet = sheet.worksheet(nombre_hoja)
    elif id_hoja:
        worksheet = sheet.get_worksheet_by_id(id_hoja)

    # Obtener todos los datos de la hoja
    data = worksheet.get_all_values()

    # Convertir los datos a un DataFrame de pandas
    df = pd.DataFrame(data[1:], columns=data[0])

    return(df)
