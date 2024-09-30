from openai import OpenAI
from variables import openai_key
import json
import pandas as pd


def clasificar_gpt(Transcripcion:str,df_categorias:pd.DataFrame,df_cuentas:pd.DataFrame)->str:
    client = OpenAI(api_key=openai_key)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
            "role": "system",
            "content": [
                {
                "type": "text",
                "text": "Eres un experto clasificador de compras donde se te pasara una transcripción realizada por otra IA donde narra las distintas compras realizadas, y debes clasificarla correctamente, dando en motivo el que se compró de la forma más normalizada que puedas, y en caso de estar disminuido el nombre, pon el nombre entero\n\nPiensa todo paso a paso"
                }
            ]
            },
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": f"{Transcripcion}"
                }
            ]
            }
        ],
        temperature=0.26,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        response_format={
            "type": "json_schema",
            "json_schema": {
            "name": "compras_response",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                "compras": {
                    "type": "array",
                    "items": {
                    "type": "object",
                    "properties": {
                        "lugar": {
                        "type": "string"
                        },
                        "motivo": {
                        "type": "string"
                        },
                        "categoria": {
                        "type": "string",
                        "enum": df_categorias['categoria'].tolist()
                        },
                        "monto": {
                        "type": "number"
                        },
                        "medio_de_pago": {
                        "type": "string",
                        "enum": df_cuentas['cuenta'].tolist()
                        },
                        "cuotas": {
                        "type": "integer"
                        }
                    },
                    "required": [
                        "lugar",
                        "motivo",
                        "categoria",
                        "monto",
                        "medio_de_pago",
                        "cuotas"
                    ],
                    "additionalProperties": False
                    }
                }
                },
                "required": [
                "compras"
                ],
                "additionalProperties": False
            }
            }
        }
    )

    Json = json.loads(response.choices[0].message.content)['compras']
    df = pd.DataFrame.from_dict(Json)
    
    
    return df