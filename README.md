# Título del proyecto
IMPLEMENTACIÓN DE RAG A TRAVÉS DE API.

## Descripción del proyecto

Esta API está diseñada para proporcionar respuestas basadas en el contexto utilizando un modelo de lenguaje de Cohere y Chroma como vector store. La solución utiliza Recuperación de Información Basada en Preguntas (RAG) para combinar capacidades de búsqueda de datos y generación de lenguaje natural.


## Instalación
--------------
Requisitos
Python 3.9 o superior
FastAPI: Framework para la construcción de la API
Cohere: Plataforma de procesamiento de lenguaje natural
Chroma: Base de datos de vectores para almacenar y recuperar información contextual

1- Clonar el repositorio
    -- git clone <url_de_mi_repo>
    --cd API-RAG

2-Crear un entorno virtual
    --python -m venv venv
    --venv\Scripts\activate

3- Instalar las dependencias
    --pip install -r requirements.txt

4-Crear variables de entorno
    -- API_KEY = tu_api_key_de_Cohere


## Uso
1- Ejecución de la aplicación
    ** uvicorn main:app --reload **

Instrucciones para utilizar el proyecto, incluyendo ejemplos de código y explicaciones de cómo funciona.

## Descripción de los endpoints

1./upload_document

-- Este endpoint permite subir documentos con un título y contenido. Los datos enviados serán procesados y almacenados (por ahora) en un archivo json para persistencia.

-- Ejemplo de solicitud:

        {
            "title": "El duende",
            "content": "Había un pequeño duende llamado Puck, conocido por su espíritu travieso..."
        }

-- Ejemplo de respuesta:

        {
            "message": "Document successfully uploaded",
            "document_id": ids[0],
        }

2. /generate_embeddings

-- Genera representaciones vectoriales (embeddings) para un fragmento de texto asociado a un documento previamente subido. Esto permite búsquedas rápidas y relevantes en la base de datos.

-- Ejemplo de solicitud:

        {
            "id": "e0786cd2-aa5d-422d-9547-d228aa14e69a"
        }

-- Ejemplo de respuesta:

        {
            "message": "Embeddings generated successfully",
            "document_id": "e0786cd2-aa5d-422d-9547-d228aa14e69a"
        }

3. /search
   
--Realiza una búsqueda en la base de datos para encontrar los documentos más relevantes basados en una consulta en texto. Devuelve un conjunto de resultados con el ID del documento, un fragmento relevante de su contenido y un puntaje de relevancia.

-- Ejemplo de solicitud:

        {
            "query": "¿Quiénes eran Sol y Luna?"
        }

-- Ejemplo de respuesta:

        {
            "results": [
                {
                    "document_id": [
                        "query-d5628936-c996-42de-ab19-1e6043b5e64b",
                        "bb941390-2ff8-47c3-b47d-5b3b47908835"
                    ],
                    "content_snippet": [
                        "¿Qué le gusta hacer a Puck?",
                        "Había un pequeño duende llamado Puck, conocido por su espíritu travieso y su amor por las bromas. Vivía en lo profundo del bosque, donde las criaturas del lugar sabían que, si algo extraño sucedía, era obra de él. Puck disfrutaba de hacer desaparecer objetos, cambiar las señales de los senderos y provocar pequeñas confusiones entre los animales. Sin embargo, su diversión nunca era malintencionada; simplemente, amaba ver las reacciones sorprendidas de los demás.\n\nUn día, decidió que quería jugarle una broma a la anciana hada que vivía cerca del arroyo. Ella, conocida por su sabiduría, siempre estaba en silencio, tejiendo sueños y pensamientos en su telar. Puck, con una sonrisa pícara, hechizó un par de hojas doradas para que se posaran sobre el telar de la hada. Cada vez que intentaba mover una hoja, esta volvía a su lugar, causando que la hada frunciera el ceño y murmurara palabras mágicas, buscando entender qué ocurría.\n\nAl ver que su broma causaba más confusión de lo esperado, Puck comenzó a sentirse un poco culpable. No quería que la hada se sintiera mal ni que su pequeña travesura interfiriera en su trabajo. Decidió entonces poner fin a la broma, pero no sin antes hacer algo más para solucionar las cosas. Usó su magia para hacer que las hojas se transformaran en pequeñas flores brillantes, que adornaron el telar y alegraron el entorno. La hada, al ver el cambio, sonrió, comprendiendo que Puck había hecho su travesura con buenas intenciones.\n\nDesde ese día, Puck aprendió que, aunque las bromas eran divertidas, también era importante ser considerado con los demás. Aunque seguía disfrutando de su naturaleza traviesa, nunca olvidó la lección que le enseñó la sabia hada: las risas compartidas son mucho más valiosas cuando se hacen con cariño y respeto."
                    ],
                    "similarity_score": 0.7138328552246094
                }
            ]
        }

4. /ask
   
-- Genera una respuesta detallada utilizando el modelo de lenguaje basado en la consulta proporcionada. Este endpoint combina la recuperación de información y la generación de texto para ofrecer respuestas personalizadas.

-- Ejemplo de solicitud:

        {
            "question": "¿Qué le gusta hacer a Puck?"
        }

-- Ejemplo de respuesta:

        {
            "answer": "A Puck le encanta jugar y hacer travesuras, ¡es muy travieso y divertido! 😁🤪🎉"
        }


