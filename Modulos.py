import pandas as pd

def Marca_temporal_a_fecha(df):
    #* Relleno la columna fecha por el dia de creacion en caso de no estar la fecha
    df['marca_temporal'] = pd.to_datetime(df['marca_temporal'],format= '%d/%m/%Y %H:%M:%S')
    df['fecha'] = pd.to_datetime(df['marca_temporal'], format= '%d/%m/%Y').dt.date
    df['fecha'] = df['fecha'].fillna(df['marca_temporal'].dt.date)
    
    return df