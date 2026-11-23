# Uso de Inteligencia Artificial Generativa en Café Match

## 1. Herramienta utilizada

Para este proyecto hemos utilizado la **API de NVIDIA**, mediante la librería `openai` y un endpoint compatible con OpenAI.

La integración se ha realizado con el modelo configurado mediante la variable `NVIDIA_MODEL`, utilizando NVIDIA Nemotron.

La IA generativa complementa nuestro modelo de Machine Learning, desarrollado con **LogisticRegression y TF-IDF**.

Mientras que el modelo de regresión logística clasifica el sentimiento general de las reseñas en positivo, negativo o neutro, NVIDIA permite interpretar las preferencias del usuario, analizar características concretas y generar explicaciones en lenguaje natural.

## 2. ¿Para qué utilizamos NVIDIA?

Hemos implementado tres funcionalidades principales.

### 2.1. Análisis de reseñas

NVIDIA analiza el texto de las reseñas e identifica opiniones relacionadas con siete características:

- Ruido.
- Ambiente.
- Bebidas.
- Comida.
- Precio.
- Comodidad.
- Atención.

Para cada característica devuelve una de las siguientes etiquetas:

`positivo`, `negativo`, `neutro` o `no_mencionado`.

La respuesta se solicita en formato JSON y se valida antes de utilizarla.

### 2.2. Interpretación de preferencias

En el modo libre de Café Match, el usuario puede describir con sus propias palabras qué tipo de cafetería está buscando.

Por ejemplo:

> Quiero una cafetería tranquila para estudiar con mi portátil, que tenga wifi y buen matcha.

NVIDIA identifica las preferencias expresadas y las devuelve en formato JSON.

En este ejemplo:

```json
{
  "quiet": true,
  "work": true,
  "wifi": true,
  "matcha": true,
  "brunch": false
}
```

Estas preferencias se utilizan para ampliar la consulta realizada por `ReviewSearch`.

También conservamos el texto original del usuario, por lo que la búsqueda no depende únicamente de las cinco preferencias definidas.

### 2.3. Explicación de recomendaciones

NVIDIA genera explicaciones breves de las cafeterías recomendadas.

Para ello recibe:

- La petición original del usuario.
- El nombre de la cafetería.
- Una reseña real recuperada por nuestro sistema de búsqueda.

El prompt indica que debe utilizar únicamente la información de la reseña, evitar inventar características y señalar cuando no dispone de información suficiente.

Por ejemplo, durante una prueba real NVIDIA explicó que Federal Cafe podía encajar porque una reseña mencionaba un ambiente adecuado para estudiar o trabajar con el ordenador.

También indicó que esa reseña no permitía confirmar si el establecimiento era tranquilo.

De esta forma, queremos que las recomendaciones sean más transparentes y estén respaldadas por evidencias.

## 3. Integración con el proyecto

La conexión con NVIDIA se encuentra en:

`starter/ia_client.py`

Hemos creado la clase `AIClient`, que contiene los siguientes métodos:

| Método | Función |
|---|---|
| `ask_nvidia()` | Realiza las peticiones a NVIDIA. |
| `analyze_review()` | Analiza características de una reseña. |
| `interpret_preferences()` | Identifica preferencias del usuario. |
| `explain_recommendation()` | Genera explicaciones basadas en reseñas reales. |

La clase dispone de dos modos de funcionamiento:

**Modo mock**

Simula las respuestas sin realizar llamadas a NVIDIA.

Se utiliza para desarrollo, pruebas automáticas y ejecución del pipeline sin depender de una API externa.

**Modo real**

Realiza llamadas a NVIDIA utilizando la clave configurada en `NVIDIA_API_KEY`.

Se utiliza para interpretar las preferencias y generar explicaciones mediante inteligencia artificial generativa.

### Integración con Machine Learning

En `starter/pipeline.py`, la clase `CafePipeline` combina:

1. Carga y validación de datos con `CafeLoader` y `CafeValidator`.
2. Predicción de sentimientos mediante `SentimentPredictor`.
3. Análisis de características mediante `AIClient`.
4. Guardado de los resultados en CSV.

Por otra parte, `CafeRecommender` combina `AIClient` y `ReviewSearch` para generar recomendaciones personalizadas a partir de las reseñas.

La selección y puntuación de cafeterías se calcula mediante nuestro código. NVIDIA se utiliza para interpretar las preferencias y explicar los resultados, no para inventar cafeterías ni asignar valoraciones.

## 4. Pruebas realizadas

Para comprobar la integración hemos realizado pruebas tanto en modo `mock` como en modo `real`.

### Modo mock

Hemos ejecutado el pipeline completo en modo simulado, procesando una reseña de cada una de las 760 cafeterías disponibles.

Los resultados se guardaron correctamente en:

`outputs/resultados_pipeline_mock.csv`

También hemos comprobado que el recomendador personalizado devuelve cafeterías con una explicación simulada.

### Modo real

Hemos realizado llamadas reales a NVIDIA para comprobar:

- La interpretación de preferencias a partir de una petición en lenguaje natural.
- El análisis de características de reseñas en la versión anterior del pipeline.
- La generación de explicaciones basadas en reseñas reales.
- La integración del recomendador personalizado con NVIDIA.

En una de las pruebas, NVIDIA identificó correctamente las preferencias de tranquilidad, trabajo, wifi y matcha.

En otra, generó una explicación de Federal Cafe a partir de una reseña real, distinguiendo entre las características mencionadas y la información no confirmada.

La nueva versión de `CafePipeline` se ha ejecutado en modo `mock`. Su ejecución completa en modo `real` queda pendiente de una comprobación específica.

### Tests automáticos

Hemos utilizado `pytest` para comprobar los distintos módulos del proyecto.

Los tests de `AIClient` utilizan respuestas simuladas mediante `monkeypatch`, evitando llamadas reales a NVIDIA.

El último resultado obtenido al ejecutar toda la batería de pruebas fue:

```text
24 passed
```

## 5. Limitaciones

El uso de IA generativa presenta algunas limitaciones.

**Interpretación de las reseñas:** NVIDIA puede interpretar incorrectamente opiniones ambiguas o identificar características que no están claramente expresadas.

**Información incompleta:** las reseñas no siempre contienen información sobre todas las preferencias del usuario. Por ejemplo, una reseña puede mencionar que una cafetería es adecuada para estudiar, pero no indicar si dispone de wifi o enchufes.

**Posibles respuestas incorrectas:** aunque los prompts indican que no debe inventar información, las explicaciones generadas deben considerarse orientativas y no una garantía absoluta.

**Coste y número de llamadas:** analizar individualmente las 103.082 reseñas mediante NVIDIA supondría muchas peticiones. Por ello, utilizamos el modelo de Machine Learning y la búsqueda TF-IDF para procesar los datos localmente, y reservamos NVIDIA para tareas concretas.

**Datos históricos:** las opiniones proceden de reseñas anteriores, por lo que algunas características de los establecimientos pueden haber cambiado.

**Preferencias iniciales:** actualmente la interpretación estructurada contempla cinco preferencias. Se mantiene también la petición original para recuperar reseñas relacionadas con otras necesidades.

## 6. Seguridad y configuración

La clave privada de NVIDIA se obtiene mediante una variable de entorno:

`NVIDIA_API_KEY`

Se utiliza un archivo `.env` local para guardar la configuración.

El archivo `.env` está excluido del repositorio mediante `.gitignore`.

Se proporciona `.env.example` para mostrar las variables necesarias sin incluir credenciales privadas.

El modo de funcionamiento se configura mediante:

`MODO_IA=mock`

o

`MODO_IA=real`

En los tests automáticos se utilizan respuestas simuladas, evitando exponer credenciales o depender de llamadas externas.

## 7. Conclusión

La integración de NVIDIA permite incorporar inteligencia artificial generativa a Café Match sin sustituir nuestro modelo de Machine Learning.

Hemos combinado clasificación de sentimientos, recuperación de reseñas y generación de explicaciones para ofrecer recomendaciones más personalizadas y comprensibles.

El objetivo es que el usuario no reciba únicamente un ranking de cafeterías, sino también información que le ayude a entender por qué podrían encajar con lo que está buscando y qué características todavía no se pueden confirmar.