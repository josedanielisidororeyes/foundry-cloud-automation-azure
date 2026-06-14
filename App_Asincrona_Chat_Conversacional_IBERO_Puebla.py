import os
from dotenv import load_dotenv

# Carga de librerías
import asyncio
from openai import AsyncOpenAI
from azure.identity.aio import DefaultAzureCredential, get_bearer_token_provider


async def main(): 

    # Limpieza de consola
    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        # Carga de credenciales
        load_dotenv()
        azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        model_deployment = os.getenv("MODEL_DEPLOYMENT")

        # Inicializaciónde cliente asincrono de OpenAI 
        credential =  DefaultAzureCredential()
        token_provider =  get_bearer_token_provider(
            credential, "https://ai.azure.com/.default"
        )

        async_client   = AsyncOpenAI(
            base_url =  azure_openai_endpoint, 
            api_key  = token_provider
        )


        

        # Seguimiento de respuestas
        last_response_id = None

        # Ciclo de chat conversacional
        while True:
            input_text = input('\nCómo te puedo ayudar (ingresa "salir" para terminar la conversación): ')
            if input_text.lower() == "salir":
                break
            if len(input_text) == 0:
                print("¿Cómo te puedo ayudar?")
                continue

            # Espera de respuesta asincrona
            response  =  await async_client.responses.create(
                model  =  model_deployment, 
                instructions  =  "Eres un asesor de admisiones de IBERO Puebla que responde de manera clara y precisa usando un lenguaje fresco y jovén",
                input  =  input_text,
                previous_response_id  =  last_response_id
            )
            assistant_text =  response.output_text
            print("Asesor:", assistant_text)
            last_response_id  =  response.id

            

    except Exception as ex:
        print(ex)

    finally:
        # Cierre de sesión de cliente asincrono
        await credential.close()




if __name__ == '__main__': 
    asyncio.run(main())