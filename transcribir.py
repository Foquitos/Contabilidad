from deepgram import DeepgramClient, PrerecordedOptions, FileSource
from variables import DEEPGRAM_API_KEY

def Transcribir(audio:str)->str:    
    deepgram = DeepgramClient(DEEPGRAM_API_KEY)
    try:
        audio = open(audio, 'rb').read()
        
        payload: FileSource = {
            "buffer": audio,
        }


        options = PrerecordedOptions(
            model="nova-2",
            language="es-419",
            punctuate=True,
            paragraphs=True,
        )
        
        response = deepgram.listen.rest.v("1").transcribe_file(payload, options)
        
        transcripcion = response['results']['channels'][0]['alternatives'][0]['transcript']
        
        return transcripcion
    except Exception as e:
        print(f"Error al transcribir {audio}: {e}")
        return None