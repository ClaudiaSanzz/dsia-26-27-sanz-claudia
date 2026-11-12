
# Uso de IA generativa en Café Match

## 1. Herramienta utilizada

Para este proyecto hemos utilizado la API de Google Gemini mediante la librería `google-genai`, con el modelo `gemini-3.5-flash-lite`.

La idea de utilizar Gemini es complementar nuestro modelo de Machine Learning, ya que el Random Forest únicamente clasifica las reseñas según su sentimiento general, mientras que Gemini nos permite analizar aspectos más concretos de cada cafetería.

## 2. ¿Para qué utilizamos Gemini?

Utilizamos Gemini para analizar el contenido de las reseñas y extraer opiniones sobre diferentes características: ruido, ambiente, bebidas, comida, precio, comodidad y atención.

Para cada una de ellas, Gemini indica si la opinión es positiva, negativa o neutra. Si la reseña no menciona esa característica, devuelve `no_mencionado`.

Esta información nos puede servir para mejorar las recomendaciones de Café Match y tener en cuenta lo que busca cada usuario.

## 3. Integración con el proyecto

La conexión con Gemini se encuentra en `cliente_ia.py`, donde hemos creado la función `analizar_resena()`.

Hemos incluido dos modos de funcionamiento:

- **Mock:** simula una respuesta sin conectarse a Gemini. Lo utilizamos para hacer pruebas sin consumir llamadas a la API.
- **Real:** envía la reseña a Gemini y devuelve el análisis de sus características en formato JSON.

El modo se selecciona mediante la variable `MODO_IA` del archivo `.env`.

Por otra parte, en `pipeline.py` hemos integrado el Random Forest y Gemini. Primero utilizamos nuestro modelo para predecir el sentimiento de la reseña y después llamamos a Gemini para analizar sus características.

Los resultados se guardan en un CSV para poder consultarlos posteriormente.

## 4. Pruebas realizadas

Para comprobar que la integración funciona, hemos ejecutado el pipeline en los dos modos.

En modo `mock` hemos procesado una reseña de cada una de las 760 cafeterías del dataset. En modo `real` hemos analizado 5 reseñas utilizando Gemini y todas las peticiones se han completado correctamente.

También hemos creado pruebas con `pytest` para comprobar la predicción del modelo, el funcionamiento del cliente en modo mock y la ejecución del pipeline.

## 5. Limitaciones

Una de las principales limitaciones es que Gemini puede interpretar mal algunas opiniones. Por ejemplo, puede confundir una crítica sobre la atención con una opinión sobre el ambiente o el precio.

Además, como estamos utilizando la API gratuita, no resulta práctico enviar las 103.082 reseñas individualmente a Gemini. Por eso, para crear los perfiles de las cafeterías hemos utilizado también búsquedas de expresiones con Python.

Otra limitación es que las reseñas son históricas, por lo que no podemos asegurar que toda la información siga siendo válida actualmente.

## 6. Seguridad

La clave de Gemini se guarda en el archivo `.env` y no aparece directamente en el código.


