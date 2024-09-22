import pandas as pd

def Marca_temporal_a_fecha(df):
    #* Relleno la columna fecha por el dia de creacion en caso de no estar la fecha
    df['Marca temporal'] = pd.to_datetime(df['Marca temporal'],format= '%d/%m/%Y %H:%M:%S')
    df['Fecha'] = pd.to_datetime(df['Fecha'], format= '%d/%m/%Y')
    df['Fecha'] = df['Fecha'].fillna(df['Marca temporal'])
    
    return df