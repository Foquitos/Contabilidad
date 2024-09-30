import pandas as pd
import numpy as np
from Modulos import Marca_temporal_a_fecha

def Egresos(df:pd.DataFrame,categorias:pd.DataFrame,medios_de_pago:pd.DataFrame)->pd.DataFrame:
    df['fecha'] = pd.Timestamp.now()
    df = pd.merge(left=df,right=categorias,how='left',left_on='categoria',right_on='categoria')
    df = pd.merge(left=df,right=medios_de_pago,how='left',left_on='medio_de_pago',right_on='cuenta')
    
    
    df = df.rename(columns={'id_x': 'categoria_id', 'id_y': 'medio_de_pago_id'})

    df['cuotas'] = df['cuotas'].replace('', np.nan).fillna(1).astype(int)

    # Expande cuota por cuota en caso de cuotas
    df['numero_de_cuota'] = df.apply(lambda row: range(1, row['cuotas'] + 1), axis=1)
    df = df.explode('numero_de_cuota')
    
    df['monto'] = pd.to_numeric(df['monto'], errors='coerce')
    df['precio'] = df['monto'] / df['cuotas']
    df['fecha_de_impacto'] = df.apply(lambda row: row['fecha'] + pd.DateOffset(months=row['numero_de_cuota'] - 1), axis=1)


    # Reorder columns
    columns_order = ['lugar', 'motivo', 'categoria_id', 'monto', 
                    'medio_de_pago_id', 'cuotas', 'numero_de_cuota', 'fecha_de_impacto', 'precio']
    df = df[columns_order]

    return df