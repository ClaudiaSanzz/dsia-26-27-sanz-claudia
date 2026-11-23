
# ☕ Café Match

Sistema de recomendación de cafeterías de Madrid que combina **Machine Learning**, búsqueda de reseñas e **inteligencia artificial generativa**.

Este proyecto constituye la base del **Proyecto III (Trabajo Final)** de DSIA.

## 1. Descripción del proyecto

**Café Match** ayuda a encontrar cafeterías de Madrid según las preferencias del usuario, utilizando opiniones reales en lugar de basarse únicamente en las valoraciones generales de los establecimientos.

El sistema combina tres tecnologías:

- **Machine Learning:** clasificación de sentimientos mediante regresión logística y TF-IDF.
- **Búsqueda de información:** recuperación de reseñas relevantes utilizando TF-IDF y similitud coseno.
- **Inteligencia Artificial Generativa:** integración con NVIDIA para interpretar preferencias y explicar recomendaciones a partir de reseñas reales.

### Modos de recomendación

| Modo | Descripción |
|---|---|
| **Focus** | Cafeterías para estudiar o trabajar. |
| **Social** | Cafeterías para conversar o quedar con amigos. |
| **Trendy** | Cafeterías relacionadas con tendencias como matcha y brunch. |
| **Surprise** | Descubrir cafeterías originales o menos conocidas. |
| **Libre** | El usuario escribe sus preferencias en lenguaje natural. |

Por ejemplo:

> Quiero una cafetería tranquila para estudiar con mi portátil y tomar un buen café.

En el modo libre, NVIDIA interpreta las preferencias, el sistema recupera reseñas relacionadas y genera un ranking de cafeterías con explicaciones.

---

## 2. Dataset

### Origen de los datos

El proyecto utiliza el dataset **TripAdvisor Restaurant Reviews**, publicado en Zenodo.

- **Autores:** Pablo Pérez-Núñez, Eva Blanco, Verónica Bolón-Canedo y Beatriz Remeseiro.
- **Fuente:** https://zenodo.org/records/14622324
- **DOI:** https://doi.org/10.5281/zenodo.14622324
- **Versión:** 2.0.0.
- **Licencia documentada:** Creative Commons Attribution 4.0 International (CC BY 4.0).
- **Fecha de descarga:** 4 de octubre de 2026.

Los datos originales contienen reseñas de restaurantes de distintas ciudades europeas.

Para Café Match se utilizaron los archivos correspondientes a Madrid.

Los archivos `items.pkl` y `reviews.pkl` se combinaron mediante `itemId`, relacionando las reseñas con los establecimientos.

Posteriormente se aplicaron los procesos de limpieza desarrollados en el Proyecto I y se seleccionaron las cafeterías.

### Datos utilizados

El dataset completo contiene **103.082 reseñas de 760 cafeterías de Madrid**.

Entre las columnas disponibles se encuentran:

| Columna | Descripción |
|---|---|
| `reviewId` | Identificador de la reseña. |
| `itemId` | Identificador de la cafetería. |
| `name` | Nombre de la cafetería. |
| `texto_review` | Texto de la reseña. |
| `rating_review` | Valoración de la reseña. |
| `rating_cafeteria` | Valoración general del establecimiento. |
| `url_review` | Enlace a la reseña original. |
| `url_cafeteria` | Enlace del establecimiento. |

### Dataset de muestra

Para evitar subir archivos demasiado grandes al repositorio, se incluye:

`data/cafeterias_muestra.csv`

Este archivo contiene **300 reseñas reales** seleccionadas para incluir ejemplos de:

- Tranquilidad y ruido.
- Estudiar o trabajar.
- Ambiente social.
- Reuniones con amigos.
- Matcha y brunch.
- Originalidad y lugares escondidos.

La muestra se genera mediante `starter/create_sample.py`.

El dataset completo se conserva localmente en:

`data/cafeterias_limpias.csv`

La muestra permite probar el pipeline y el recomendador sin disponer de las 103.082 reseñas originales.

**Importante:** esta muestra se ha seleccionado para demostrar las funcionalidades, no para representar estadísticamente el dataset completo ni reproducir las métricas del entrenamiento.

### Motivación

Se eligió este dataset porque contiene reseñas escritas por usuarios reales y valoraciones numéricas.

Esto permite combinar:

1. Clasificación de sentimientos con scikit-learn.
2. Búsqueda de opiniones relevantes mediante TF-IDF.
3. Recomendaciones personalizadas.
4. Explicaciones generadas mediante NVIDIA.

Además, este mismo dominio se utilizará para desarrollar el Proyecto III.

---

## 3. Preparación de datos

La preparación se realiza mediante tres clases:

- `CafeLoader`: carga los archivos CSV.
- `CafeValidator`: comprueba las columnas y elimina reseñas sin texto.
- `DataPreparation`: selecciona las variables, elimina textos duplicados para el entrenamiento y asigna las etiquetas de sentimiento.

Las etiquetas se obtienen a partir de `rating_review`:

| Valoración | Sentimiento |
|---|---|
| 10 o 20 | Negativo |
| 30 | Neutro |
| 40 o 50 | Positivo |

Los textos duplicados se eliminan durante la preparación de los datos de entrenamiento, pero las reseñas originales siguen disponibles para crear perfiles y recomendaciones.

---

## 4. Modelo de Machine Learning

Se utiliza un clasificador de sentimientos desarrollado con **scikit-learn**.

### Modelo seleccionado

- **Algoritmo:** `LogisticRegression`.
- **Representación del texto:** `TfidfVectorizer`.
- **Número máximo de características:** 10.000.
- **Iteraciones máximas:** 1.000.
- **Semilla de partición:** `random_state=42`.

Inicialmente se utilizó Random Forest como alternativa, pero finalmente se seleccionó regresión logística por su mejor rendimiento en validación y menor complejidad computacional.

### División de datos

Se utiliza una división estratificada:

| Conjunto | Porcentaje |
|---|---:|
| Entrenamiento | 60 % |
| Validación | 20 % |
| Test | 20 % |

El vectorizador TF-IDF se ajusta únicamente utilizando los datos de entrenamiento.

### Resultados

| Métrica | Validación | Test |
|---|---:|---:|
| Accuracy | 0.8502 | 0.8523 |
| F1-macro | 0.6859 | 0.6876 |

El modelo obtiene una **accuracy del 85,23 % en test**.

El F1-macro indica que existen diferencias de rendimiento entre las clases, especialmente por la dificultad de clasificar reseñas neutras y el desequilibrio del dataset.

Las métricas completas se guardan en:

`outputs/metrics.json`

Este archivo incluye el informe de clasificación y la matriz de confusión.

### Guardado del modelo

El entrenamiento genera dos archivos mediante `joblib`:

- `models/model.joblib`: modelo de regresión logística.
- `models/vectorizer.joblib`: vectorizador TF-IDF.

**Ambos archivos están incluidos en GitHub**, por lo que se pueden realizar predicciones sin volver a entrenar.

---

## 5. Sistema de recomendaciones

### Perfiles de cafeterías

La clase `CafeProfiles`, implementada en `starter/profiles.py`, analiza las reseñas y genera perfiles de los establecimientos.

Se identifican menciones relacionadas con:

- Tranquilidad y ruido.
- Estudiar o trabajar.
- Ambiente social.
- Grupos de amigos.
- Matcha y brunch.
- Originalidad.
- Lugares escondidos.

Los perfiles se pueden guardar en:

`outputs/perfiles_cafeterias.csv`

Cuando se ejecuta el recomendador, los perfiles se generan directamente a partir del dataset utilizado para evitar mezclar información del conjunto completo con la muestra.

### Búsqueda mediante TF-IDF

La clase `ReviewSearch` permite recuperar reseñas relacionadas con la petición del usuario.

El proceso consiste en:

1. Transformar la consulta utilizando TF-IDF.
2. Calcular la similitud coseno con las reseñas.
3. Seleccionar las reseñas relevantes.
4. Utilizar el modelo de sentimientos para identificar opiniones clasificadas como positivas.
5. Seleccionar hasta tres reseñas por cafetería.
6. Calcular una puntuación de relevancia suavizada.

También se recupera una reseña real que se utiliza para explicar la recomendación.

### Ranking personalizado

La clase `CafeRecommender` permite recomendar cafeterías mediante cuatro modos predefinidos o una petición libre.

En el modo libre se combinan:

- Relevancia de las reseñas recuperadas.
- Evidencias disponibles.
- Valoración general de la cafetería.

La puntuación final experimental utiliza:

- **70 %:** relevancia relativa de la búsqueda.
- **30 %:** valoración general ponderada.

Los pesos todavía no han sido optimizados mediante una evaluación formal.

**La puntuación final es un valor de ranking, no una probabilidad de satisfacción.**

---

## 6. Inteligencia Artificial Generativa: NVIDIA

El proyecto integra la API de **NVIDIA** mediante la librería `openai`, utilizando un endpoint compatible con OpenAI.

La integración se encuentra en:

`starter/ia_client.py`

### Funcionalidades

La clase `AIClient` implementa tres funcionalidades principales.

#### Análisis de reseñas

NVIDIA analiza siete características:

- Ruido.
- Ambiente.
- Bebidas.
- Comida.
- Precio.
- Comodidad.
- Atención.

Para cada característica devuelve una etiqueta:

`positivo`, `negativo`, `neutro` o `no_mencionado`.

#### Interpretación de preferencias

En el modo libre, NVIDIA interpreta las preferencias del usuario, identificando características como:

- Tranquilidad.
- Estudiar o trabajar.
- Wifi.
- Matcha.
- Brunch.

El sistema conserva también el texto original de la petición para realizar la búsqueda de reseñas.

#### Explicación de recomendaciones

NVIDIA genera explicaciones breves basadas en una reseña real recuperada por el sistema.

El objetivo es justificar las recomendaciones sin inventar características que no estén respaldadas por las opiniones.

### Modos de funcionamiento

| Modo | Descripción |
|---|---|
| `mock` | Simula las respuestas sin conectarse a NVIDIA. |
| `real` | Realiza llamadas a NVIDIA para analizar reseñas, interpretar preferencias y generar explicaciones. |

El modo `mock` permite desarrollar, ejecutar pruebas y demostrar el proyecto sin consumir llamadas a la API.

El modo `real` utiliza inteligencia artificial generativa y necesita una clave de NVIDIA válida.

### Pruebas realizadas

Hemos comprobado el pipeline en ambos modos.

En modo `mock`:

- Se procesaron 760 cafeterías utilizando el dataset completo.
- Se procesaron 145 cafeterías utilizando la muestra.

En modo `real`:

- Se analizaron cinco reseñas de cinco cafeterías.
- Las cinco peticiones a NVIDIA devolvieron HTTP 200.
- Los resultados se guardaron en `outputs/resultados_pipeline_real.csv`.
- Se generó un resumen mediante `starter.review_summary`.

También se comprobó el recomendador en modo `real`, verificando que NVIDIA interpreta preferencias y genera explicaciones basadas en reseñas recuperadas.

El archivo `AI_USAGE.md` contiene información adicional sobre la integración de IA y las pruebas realizadas.

---

## 7. Estructura del proyecto

La estructura principal es:

    Proyecto_ii/
    ├── starter/
    │   ├── __init__.py
    │   ├── loader.py
    │   ├── validator.py
    │   ├── data_preparation.py
    │   ├── train.py
    │   ├── predict.py
    │   ├── profiles.py
    │   ├── review_search.py
    │   ├── recommender.py
    │   ├── ia_client.py
    │   ├── pipeline.py
    │   ├── review_summary.py
    │   └── create_sample.py
    │
    ├── tests/
    │   ├── test_predict.py
    │   ├── test_profiles.py
    │   ├── test_review_search.py
    │   ├── test_ia_client.py
    │   ├── test_recommender.py
    │   └── test_pipeline.py
    │
    ├── data/
    │   └── cafeterias_muestra.csv
    │
    ├── models/
    │   ├── model.joblib
    │   └── vectorizer.joblib
    │
    ├── outputs/
    │   └── metrics.json
    │
    ├── .env.example
    ├── .gitignore
    ├── requirements.txt
    ├── AI_USAGE.md
    └── README.md

El dataset completo y los CSV generados durante la ejecución se conservan localmente y no se incluyen en el repositorio.

---

## 8. Instalación

El proyecto utiliza Python, scikit-learn y la API de NVIDIA.

La instalación se ha probado con Python 3.14.7 y `uv` desde un clon nuevo de GitHub.

### Crear el entorno virtual

Desde `Proyecto_ii`:

    uv venv

Activar el entorno en Git Bash:

    source .venv/Scripts/activate

### Instalar dependencias

    uv pip install -r requirements.txt

Las principales librerías utilizadas son:

- `pandas`
- `numpy`
- `scikit-learn`
- `joblib`
- `openai`
- `python-dotenv`
- `pytest`

### Configuración de NVIDIA

El repositorio incluye `.env.example`.

Para ejecutar NVIDIA en modo real, crear un archivo `.env` local con:

    MODO_IA=real
    NVIDIA_API_KEY=TU_CLAVE_AQUI
    NVIDIA_MODEL=nvidia/nemotron-3.5-super-vl-120b-a12b

El archivo `.env` contiene información privada y no debe subirse a GitHub.

Para ejecutar sin utilizar NVIDIA se puede configurar:

    MODO_IA=mock

---

## 9. Ejecución del proyecto

Todos los comandos deben ejecutarse desde la carpeta `Proyecto_ii`, con el entorno virtual activado.

### 9.1. Entrenar el modelo

Requiere el dataset completo en:

`data/cafeterias_limpias.csv`

Comando:

    python -m starter.train

Este comando:

1. Carga y valida los datos.
2. Prepara las etiquetas de sentimiento.
3. Divide los datos en entrenamiento, validación y test.
4. Entrena la regresión logística.
5. Calcula las métricas.
6. Guarda el modelo y el vectorizador.

### 9.2. Generar perfiles

    python -m starter.profiles

Utiliza el dataset completo si existe y, en caso contrario, la muestra de 300 reseñas.

Genera:

`outputs/perfiles_cafeterias.csv`

### 9.3. Ejecutar el pipeline

**Modo mock:**

    MODO_IA=mock python -m starter.pipeline

**Modo real:**

    MODO_IA=real python -m starter.pipeline

El pipeline:

1. Carga las reseñas.
2. Valida las columnas.
3. Selecciona una reseña por cafetería.
4. Predice el sentimiento utilizando el modelo sklearn.
5. Analiza las características con NVIDIA o su versión simulada.
6. Guarda los resultados en CSV.

Los resultados se guardan en:

- `outputs/resultados_pipeline_mock.csv`
- `outputs/resultados_pipeline_real.csv`

El pipeline incluye logs de inicio, progreso y finalización.

En modo `real` se limita el análisis a cinco reseñas para evitar llamadas innecesarias a la API.

### 9.4. Ejecutar el recomendador

**Modo mock:**

    MODO_IA=mock python -m starter.recommender

**Modo real con NVIDIA:**

    MODO_IA=real python -m starter.recommender

Al iniciar el programa aparece:

    CAFÉ MATCH
    Modos: focus, social, trendy, surprise, libre
    Elige un modo:

En el modo libre, el usuario escribe lo que busca.

Por ejemplo:

    Quiero una cafetería tranquila para estudiar

El sistema interpreta las preferencias, recupera reseñas relevantes y devuelve hasta tres cafeterías con su valoración, puntuación y explicación.

### 9.5. Generar resumen de opiniones

Después de ejecutar el pipeline en modo `real`:

    python -m starter.review_summary

Este comando utiliza:

`outputs/resultados_pipeline_real.csv`

Y genera:

`outputs/resumen_opiniones.csv`

El resumen contiene los conteos de opiniones positivas y negativas por característica y cafetería.

### 9.6. Generar la muestra

Si se dispone del dataset completo:

    python -m starter.create_sample

Genera:

`data/cafeterias_muestra.csv`

La muestra contiene 300 reseñas reales seleccionadas para incluir características útiles en los diferentes modos de recomendación.

---

## 10. Reproducibilidad

El proyecto permite dos formas de ejecución.

### Ejecución con el dataset completo

Si existe:

`data/cafeterias_limpias.csv`

El pipeline y el recomendador utilizan las 103.082 reseñas originales.

### Ejecución con la muestra

Si no existe el dataset completo, utilizan automáticamente:

`data/cafeterias_muestra.csv`

De esta manera, el proyecto puede ejecutarse directamente después de clonar GitHub.

Los perfiles se generan a partir del mismo dataset utilizado para las recomendaciones, evitando mezclar información de distintas versiones.

### Comprobación desde GitHub

Se realizó una instalación limpia del repositorio:

1. Clonación desde GitHub.
2. Creación de un entorno virtual.
3. Instalación de las dependencias.
4. Ejecución del recomendador en modo `mock`.
5. Ejecución de los tests automáticos.

La aplicación detectó correctamente la muestra y generó tres recomendaciones.

**La muestra permite probar el sistema, pero no reproducir las métricas originales del entrenamiento completo.**

---

## 11. Tests y calidad

El proyecto utiliza `pytest` para comprobar el funcionamiento de sus componentes.

Se incluyen pruebas para:

- Predicción de sentimientos.
- Generación de perfiles.
- Búsqueda de reseñas.
- Cliente de NVIDIA.
- Recomendador personalizado.
- Ejecución del pipeline.

Para ejecutar todos los tests:

    python -m pytest -q

Último resultado comprobado:

    24 passed

Los 24 tests también se superaron desde una instalación limpia de GitHub.

Los tests automáticos no realizan llamadas reales a NVIDIA, evitando depender de una conexión externa o de una clave privada.

---

## 12. Limitaciones

El proyecto presenta algunas limitaciones:

- TF-IDF depende de coincidencias entre palabras y no interpreta completamente el significado de los textos.
- Una reseña positiva puede contener comentarios negativos sobre características concretas.
- Las preferencias detectadas no se verifican todavía de forma individual para cada cafetería.
- La relevancia de una reseña no garantiza que el establecimiento cumpla todas las preferencias.
- Los pesos del ranking son experimentales y requieren evaluación adicional.
- Las reseñas son históricas, por lo que algunas características pueden haber cambiado.
- NVIDIA puede generar interpretaciones incorrectas y sus explicaciones deben considerarse orientativas.
- La muestra de 300 reseñas permite demostrar el funcionamiento, pero no representa estadísticamente el dataset completo.

---

## 13. Continuidad hacia el Proyecto III

El Proyecto II constituye la base técnica del **Proyecto III (Trabajo Final)**.

En esta entrega ya se han desarrollado:

- Carga y validación de datos.
- Pipeline automatizado con logs.
- Modelo de Machine Learning entrenado.
- Persistencia e inferencia del modelo.
- Sistema de recomendación.
- Integración de NVIDIA en modo `mock` y `real`.
- Tests automáticos.
- Configuración y documentación del proyecto.

### Mejoras previstas para el Proyecto III

#### Aplicación interactiva con Streamlit

Se desarrollará una interfaz para que los usuarios puedan introducir sus preferencias y visualizar las cafeterías recomendadas.

#### API con FastAPI

Se plantea incorporar una API que permita consultar recomendaciones y predicciones del modelo, además de exponer operaciones de análisis con IA generativa.

#### Validación y gestión de errores

Se ampliará la validación de entradas, las respuestas de error y la robustez de las llamadas a servicios externos.

#### Integración continua y despliegue

Se incorporarán herramientas para ejecutar tests automáticamente y facilitar el despliegue de la aplicación.

#### Monitorización

Se estudiará cómo registrar errores, tiempos de respuesta, uso de la API y comportamiento de las recomendaciones.

El objetivo es reutilizar los componentes desarrollados en el Proyecto II sin tener que reescribir el núcleo del sistema.

Estas funcionalidades corresponden a la ampliación prevista y no se presentan como ya implementadas.

---

## 14. Referencias

- Pérez-Núñez, P., Blanco, E., Bolón-Canedo, V. y Remeseiro, B. *TripAdvisor Restaurant Reviews*, versión 2.0.0. Zenodo. https://doi.org/10.5281/zenodo.14622324
- Creative Commons. *Attribution 4.0 International (CC BY 4.0).* https://creativecommons.org/licenses/by/4.0/
- Documentación adicional del uso de inteligencia artificial: [AI_USAGE.md](AI_USAGE.md)
