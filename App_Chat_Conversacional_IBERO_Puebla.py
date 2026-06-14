# Creación de un chat conversacional para IBERO Puebla

# Importación de librerías
import os
from dotenv import load_dotenv

from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

def main():
    # Limpiar consola
    os.system("cls" if os.name == "nt" else "clear")

    try:
        # Obtener configuración del proyecto
        load_dotenv()
        azure_openai_endpoint  =  os.getenv("AZURE_OPENAI_ENDPOINT")
        model_deployment  =  os.getenv("MODEL_DEPLOYMENT")

        # Inicialización del cliente de OpenAI
        token_provider =  get_bearer_token_provider(
            DefaultAzureCredential(), "https://ai.azure.com/.default"
        )
        openai_client =  OpenAI(
            base_url  =  azure_openai_endpoint,
            api_key  =  token_provider
        )

        # Ciclo para salir del chat conversacional
        last_response_id  =  None
        while True:
            input_text =  input("\n Hola soy Ignacio:  ¿Cómo te puedo ayudar (ingresa 'salir' para terminar la conversación): ")
            if input_text == "salir":
                break
            if len(input_text) == 0:
                print("¿Cómo te puedo ayudar?")
                continue
            # Obtener una respuesta
            stream  =  openai_client.responses.create(
                model  =  model_deployment, 
                instructions  =  "Eres un asesor de admisiones de IBERO Puebla que responde de manera clara y precisa usando un lenguaje clara y fresco.",
                input  =  input_text,
                previous_response_id   =  last_response_id,
                stream =  True
            )
            for event in stream:
                if event.type  == "response.output_text.delta":
                    print(event.delta, end  =  "")
                elif event.type ==  "response.completed":
                    last_response_id =  event.response.id


    except  Exception as ex:
        print(ex)

if __name__ == "__main__":
    main()
    