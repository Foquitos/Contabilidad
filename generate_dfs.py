from generales import sheet_a_dataframe
from Egresos import Egresos
from Modulos import Marca_temporal_a_fecha
from Dolar_MEP import Obtener_Mep
import pandas as pd

def generar_dfs():
    df_egresos_crudo = sheet_a_dataframe('1vL8vY47_K6zX-mh1KAkiOMjpi4Njl4fQqkoknvIu3YU','Egresos')
    df_ingresos_crudo = sheet_a_dataframe('1DSGdjhRruts7vV2nGdDnTgfri9iYICWcm4NL7XPtBqU','Ingresos')
    df_transferencias_crudo = sheet_a_dataframe('1BYFbo-gROoPDz6_El2HpY-_3UKZY6fL5ajcZbWX6Sq4','Respuestas de formulario 1')
    df_dolar = Obtener_Mep()
    df_fechas_creditos = sheet_a_dataframe('1-0R7ZR-v5bM04Whr6b0fleZ3AU9-GnGSDH4M-ZNtY2U','Fechas')
    df_fechas_creditos['Cierre'] = pd.to_datetime(df_fechas_creditos['Cierre'], format= '%d/%m/%Y')
    df_fechas_creditos['Vencimiento'] = pd.to_datetime(df_fechas_creditos['Vencimiento'], format= '%d/%m/%Y')

    df_egresos = Egresos(df=df_egresos_crudo,df_ingresos=df_ingresos_crudo,df_fechas=df_fechas_creditos,dolar=df_dolar)
    df_ingresos = Marca_temporal_a_fecha(df_ingresos_crudo)
    df_transferencias = Marca_temporal_a_fecha(df_transferencias_crudo)
    
    return df_egresos, df_ingresos, df_transferencias


