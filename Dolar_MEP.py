import requests
import pandas as pd
from datetime import datetime

def Obtener_Mep():
    # Obtén la fecha actual en el formato adecuado
    fecha_actual = datetime.today().strftime('%Y-%m-%d')

    # Define la URL con la fecha actual
    url = f"https://mercados.ambito.com/dolarrava/mep/grafico/2023-09-01/{fecha_actual}"

    # Agrega un User-Agent válido para emular un navegador
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
    }

    # Realiza la solicitud con el encabezado de User-Agent
    response = requests.get(url, headers=headers)

    # Verifica si la solicitud fue exitosa
    if response.status_code == 200:
        # Decodifica la respuesta como JSON
        data = response.json()

        # Convierte los datos en un DataFrame
        df_dolar_mep = pd.DataFrame(data[1:], columns=["Fecha", "DOLAR MEP"])

        # Asegúrate de convertir la columna de fecha a tipo datetime
        df_dolar_mep['Fecha'] = pd.to_datetime(df_dolar_mep['Fecha'], format='%d/%m/%Y')

        # Muestra el DataFrame
        return df_dolar_mep
        
    else:
        print(f"Error: Solicitud fallida con código de estado {response.status_code}")