import os
from dotenv import load_dotenv
import glob

# Import namespaces
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

def main(): 
    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        # Get configuration settings 
        load_dotenv()
        azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        model_deployment = os.getenv("MODEL_DEPLOYMENT")

        # Initialize the OpenAI client
        token_provider =  get_bearer_token_provider(
            DefaultAzureCredential(), "https://ai.azure.com/.default"
        )
        openai_client =  OpenAI(
            base_url  =  azure_openai_endpoint,
            api_key  =  token_provider

        )
        file_stream  = [open(f, "rb") for f in glob.glob("C:/Users/reyes/Downloads/Certificación_AI_103/Folletos_Admisiones/*.pdf")]
        if not file_stream:
            print("No hay archivos PDF")
            return
        
        # Create vector store and upload files
        print("Creando vector, subiendo archivos ...")
        vector_store =  openai_client.vector_stores.create(
            name =  "folletos-admisiones"
        )

        
        file_batch  =  openai_client.vector_stores.file_batches.upload_and_poll(
            vector_store_id = vector_store.id,
            files =  file_stream
        )

        for file in file_stream:
            file.close()
        print(f"Vector creado con {file_batch.file_counts.completed} archivos")



        


        # Track conversation state
        last_response_id = None

        # Loop until the user wants to quit
        while True:
            input_text = input('\nCómo te puedo ayudar (ingresa "salir" para finalizar la conversación): ')
            if input_text.lower() == "salir":
                break
            if len(input_text) == 0:
                print("Cómo te puedo ayudar.")
                continue

            # Get a response using tools
            response  =  openai_client.responses.create(
                model  =  model_deployment, 
                instructions =  """
                Eres un asesor de admisiones de IBERO Puebla que brinda informacíon de manera clara y concisa 
                usando los folletos de admisiones. Tambien puedes buscar información en la web de la oferta
                académica de Anáhuac Puebla, UPAEP, UDLAP y Tecnológico de Monterrey Puebla para dar un mejor respuesta.
                Tu objetivo es asegurar que el aspirante se inscriba en IBERO Puebla. Utiliza un lenguaje fresco. 
                
                """,
                input =  input_text, 
                previous_response_id  =  last_response_id,
                tools  =  [
                    {
                        "type": "file_search",
                        "vector_store_ids": [vector_store.id]
                    },
                    {
                        "type": "web_search"
                    }
                ]
            )
            print(response.output_text)
            last_response_id  = response.id
           
            



    except Exception as ex:
        print(ex)

if __name__ == '__main__': 
    main()
