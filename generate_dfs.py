from Egresos import Egresos
from Dolar_MEP import Obtener_Mep
import pandas as pd
from chat_gpt import clasificar_gpt
from variables import engine
from transcribir import Transcribir

def generar_dfs(audio):
    categorias = pd.read_sql('select * from categorias_egresos',engine)
    medios_de_pago = pd.read_sql('select * from cuentas',engine)

    transcripcion = Transcribir(audio=audio)

    df_egresos_crudo = clasificar_gpt(
        Transcripcion=transcripcion,
        df_categorias=categorias,
        df_cuentas=medios_de_pago)
    df_egresos = Egresos(
        df=df_egresos_crudo,
        categorias=categorias,
        medios_de_pago=medios_de_pago)
    
    return df_egresos



df1 = generar_dfs(audio=r'Audio de WhatsApp 2024-09-29 a las 19.26.09_0aed3ac3.waptt.opus')
print(df1)
# df1.to_sql('Egresos',engine,index=False)




