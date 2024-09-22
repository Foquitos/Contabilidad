import pandas as pd
import numpy as np
from Modulos import Marca_temporal_a_fecha

def ultimo_jueves_del_mes(fecha):
    """
    Dada una fecha, encuentra el último jueves del mes.
    """
    # Empezamos desde el último día del mes y retrocedemos hasta encontrar un jueves
    ultimo_dia = fecha.replace(day=1) + pd.DateOffset(months=1) - pd.DateOffset(days=1)
    while ultimo_dia.weekday() != 3:  # 3 es el número que representa el jueves (lunes=0, martes=1, etc.)
        ultimo_dia -= pd.DateOffset(days=1)
    return ultimo_dia

def asignar_fecha_pago(df, df_tarjetas,dolar):
    df['Fecha de pago'] = pd.NaT
    df_tarjetas = df_tarjetas.sort_values(by='Cierre')
    dolar = dolar.sort_values(by='Fecha')
    

    # Iteramos sobre cada compra y asignamos las fechas correspondientes
    for i, row in df.iterrows():
        tarjeta = row['Medio de pago']
        
        # Filtramos las fechas de la tarjeta actual
        tarjeta_info = df_tarjetas[df_tarjetas['Tarjeta'] == tarjeta]
        
        if not tarjeta_info.empty:
            # Iteramos sobre los ciclos de facturación
            for _, ciclo in tarjeta_info.iterrows():
                cierre = ciclo['Cierre']
                vencimiento = ciclo['Vencimiento']

                # Si la fecha de impacto está después del cierre actual y antes del próximo cierre
                if row['Fecha de impacto'] <= cierre:
                    # Asignamos la fecha de cierre y vencimiento
                    df.at[i, 'Fecha de pago'] = vencimiento
                    break
        else:
            # Si no se encuentra la tarjeta, verificamos si es una tarjeta de crédito
            if 'crédito' in tarjeta.lower():
                # Asignar el último jueves del mes de la fecha de impacto
                cierre_asignado = ultimo_jueves_del_mes(row['Fecha de impacto'])
                # Asignar como fecha de vencimiento 10 días después del cierre
                df.at[i, 'Fecha de pago'] = cierre_asignado + pd.DateOffset(days=10)
            else:
                df.at[i, 'Fecha de pago'] = row['Fecha de impacto']
        
        for _, ciclo in dolar.iterrows():
                fecha = ciclo['Fecha']
                Precio_dolar = ciclo['DOLAR MEP']

                # Si la fecha de impacto está después del cierre actual y antes del próximo cierre
                if row['Fecha de impacto'] <= fecha:
                    # Asignamos la fecha de cierre y vencimiento
                    df.at[i, 'Precio dolar'] = row['Precio'] / Precio_dolar
                    df.at[i, 'Gasto dolar'] = row['Gasto'] / Precio_dolar
                    break

    return df


def Egresos(df,df_ingresos,df_fechas,dolar):
    #* Relleno la columna fecha por el dia de creacion en caso de no estar la fecha
    df = Marca_temporal_a_fecha(df)

    #* Reemplazo en caso de ser una categoria Otro por lo que dice la columna Otro
    #TODO Esto a sacar en un futuro en caso de que se realice directamnete sobre una base distinta
    df['Categoria'] = df.apply(lambda row: row['Otro'] if row['Categoría'] == 'Otro' else row['Categoría'], axis=1)
    df = df.drop(['Otro',], axis=1)

    # Reemplaza coma por punto para evitar errores y los caracteres vacio por 1 en cuotas 
    df['Monto total'] = df['Monto total'].str.replace(',', '.').astype(float)
    df['Cuotas'] = df['Cuotas'].replace('', np.nan).fillna(1).astype(int)

    # Expande cuota por cuota en caso de cuotas
    df['Numero de cuota'] = df.apply(lambda row: range(1, row['Cuotas'] + 1), axis=1)
    df = df.explode('Numero de cuota')
    df['Precio'] = df['Monto total'] / df['Cuotas']
    df['Fecha de impacto'] = df.apply(lambda row: row['Fecha'] + pd.DateOffset(months=row['Numero de cuota'] - 1), axis=1)

    # Añade un indice
    df = df.reset_index(drop=True)
    df = df.reset_index(drop=False)
    df['index'] = df['index'].astype(int)

    # Reorder columns
    columns_order = ['index', 'Marca temporal', 'Fecha', 'Lugar', 'Motivo', 'Categoria', 'Monto total', 
                    'Medio de pago', 'Cuotas', 'Numero de cuota', 'Fecha de impacto', 'Precio']
    df = df[columns_order]

    # Compara los gastos con los ingresos para diferenciar gasto de precio
    df_ingresos['Gasto conjunto id'] = pd.to_numeric(df_ingresos['Gasto conjunto id'], errors='coerce')
    df_ingresos['Monto'] = pd.to_numeric(df_ingresos['Monto'], errors='coerce')
    df_ingresos = df_ingresos.groupby('Gasto conjunto id')['Monto'].sum().reset_index()
    df = df.merge(df_ingresos[['Gasto conjunto id', 'Monto']], 
                left_on='index', right_on='Gasto conjunto id', how='left')

    df['Monto'] = df['Monto'].fillna(0)
    df['Gasto'] = df['Precio'] - df['Monto']

    # Borra las columnas innecesarias
    df = df.drop(['Monto','Gasto conjunto id'], axis=1)

    df = asignar_fecha_pago(df=df,df_tarjetas=df_fechas,dolar=dolar)

    # Display the result
    return df