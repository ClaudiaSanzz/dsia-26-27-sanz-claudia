# Café Match

Sistema inteligente de recomendación de cafeterías en Madrid mediante Machine Learning e Inteligencia Artificial Generativa.

## 1. Descripción del proyecto

**Café Match** es un sistema de recomendación que ayuda a los usuarios a encontrar cafeterías de Madrid según sus necesidades y preferencias.

El proyecto combina tres tecnologías principales:

- **Machine Learning:** clasificación del sentimiento de las reseñas mediante regresión logística.
- **Búsqueda de información:** recuperación de reseñas relevantes utilizando TF-IDF y similitud coseno.
- **Inteligencia Artificial Generativa:** integración con NVIDIA para interpretar preferencias y explicar recomendaciones utilizando reseñas reales.

El objetivo es ofrecer recomendaciones personalizadas y justificadas, en lugar de basarse únicamente en las valoraciones generales de las cafeterías.

### Modos de recomendación

El sistema dispone de cinco opciones:

| Modo | Descripción |
|---|---|
| **Focus** | Cafeterías para estudiar o trabajar, priorizando tranquilidad y comodidad. |
| **Social** | Cafeterías para conversar o quedar con amigos. |
| **Trendy** | Cafeterías relacionadas con tendencias como el matcha o el brunch. |
| **Surprise** | Descubrir cafeterías originales o menos conocidas. |
| **Libre** | El usuario describe sus preferencias con sus propias palabras. |

En el modo libre, el usuario puede introducir una petición como:

> Quiero una cafetería tranquila para estudiar con mi portátil, que tenga wifi y buen matcha.

NVIDIA interpreta las preferencias expresadas y el sistema busca reseñas relacionadas para generar un ranking de cafeterías.

---

## 2. Dataset

Se utiliza un dataset de **103.082 reseñas de 760 cafeterías de Madrid**.

Entre las columnas disponibles se encuentran:

- `reviewId`: identificador de la reseña.
- `itemId`: identificador de la cafetería.
- `name`: nombre de la cafetería.
- `texto_review`: contenido de la reseña.
- `rating_review`: valoración de la reseña.
- `rating_cafeteria`: valoración general del establecimiento.
- `url_review`: enlace a la reseña original.
- `url_cafeteria`: enlace del establecimiento.

### Dataset de muestra

Para evitar subir archivos demasiado grandes al repositorio, se incluye:

`data/cafeterias_muestra.csv`

Esta muestra contiene **300 reseñas (212 KB)**, distribuidas de forma equilibrada entre sentimientos positivos, negativos y neutros.

El dataset completo se conserva localmente en:

`data/cafeterias_limpias.csv`

**Importante:** la muestra sirve para inspeccionar la estructura de los datos y realizar pruebas limitadas. No permite reproducir las métricas del entrenamiento completo.

El dataset original no se incluye en el repositorio debido a su tamaño. Para reproducir el entrenamiento completo es necesario disponer de ese archivo.

---

## 3. Preparación de datos

La preparación se realiza mediante las clases:

- `CafeLoader`: carga los archivos CSV.
- `CafeValidator`: comprueba las columnas y elimina reseñas sin texto.
- `DataPreparation`: selecciona las variables necesarias, elimina textos duplicados y asigna las etiquetas de sentimiento.

Los sentimientos se obtienen a partir de `rating_review`:

| Valoración | Sentimiento |
|---|---|
| 10 o 20 | Negativo |
| 30 | Neutro |
| 40 o 50 | Positivo |

La eliminación de textos duplicados se aplica a los datos utilizados para entrenar el modelo, sin eliminar esas reseñas del dataset original utilizado para generar perfiles.

---

## 4. Modelo de Machine Learning

Se ha desarrollado un clasificador de sentimientos con **scikit-learn**.

### Modelo seleccionado

- Algoritmo: `LogisticRegression`.
- Representación del texto: `TfidfVectorizer`.
- Número máximo de características: 10.000.
- Iteraciones máximas: 1.000.
- Semilla de partición: `random_state=42`.

Se utilizó inicialmente Random Forest como alternativa, pero finalmente se seleccionó regresión logística por su mejor rendimiento en validación y su menor complejidad computacional.

### División de datos

Los datos se dividen en tres conjuntos:

| Conjunto | Porcentaje |
|---|---:|
| Entrenamiento | 60 % |
| Validación | 20 % |
| Test | 20 % |

La división utiliza estratificación para mantener aproximadamente la proporción de las tres clases.

El vectorizador TF-IDF se ajusta únicamente con los datos de entrenamiento.

### Resultados

| Métrica | Validación | Test |
|---|---:|---:|
| Accuracy | 0.8502 | 0.8523 |
| F1-macro | 0.6859 | 0.6876 |

El modelo alcanza una **accuracy del 85,23 % en test**.

El F1-macro es menor, lo que indica que el rendimiento no es igual para las tres categorías. Una de las principales dificultades es la clasificación de reseñas neutras y el desequilibrio entre clases.

Las métricas completas, incluyendo precision, recall, F1-score por clase y matriz de confusión, se guardan en:

`outputs/metrics.json`

### Guardado del modelo

El entrenamiento genera dos archivos mediante `joblib`:

- `models/model.joblib`: modelo de regresión logística.
- `models/vectorizer.joblib`: vectorizador TF-IDF entrenado.

Estos archivos se utilizan posteriormente para realizar predicciones sin volver a entrenar el modelo.

---

## 5. Sistema de recomendaciones

Café Match combina diferentes componentes para generar recomendaciones.

### Perfiles de cafeterías

La clase `CafeProfiles` analiza las reseñas y genera perfiles con información sobre las cafeterías.

Se identifican menciones relacionadas con:

- Tranquilidad y ruido.
- Posibilidad de estudiar o trabajar.
- Ambiente social.
- Reuniones con amigos.
- Matcha y brunch.
- Originalidad y descubrimiento.

Los perfiles se guardan en:

`outputs/perfiles_cafeterias.csv`

### Búsqueda mediante TF-IDF

La clase `ReviewSearch` permite recuperar reseñas relacionadas con una petición escrita en lenguaje natural.

El funcionamiento es:

1. Se transforma la petición del usuario utilizando el vectorizador TF-IDF.
2. Se calcula la similitud coseno con las reseñas.
3. Se conservan las reseñas relacionadas con la búsqueda.
4. Se utiliza el modelo de sentimientos para seleccionar opiniones clasificadas como positivas.
5. Se seleccionan hasta tres reseñas por cafetería.
6. Se calcula una puntuación de relevancia suavizada para evitar depender exclusivamente de una sola opinión.

También se recupera una reseña real que puede utilizarse como evidencia de la recomendación.

### Ranking personalizado

La clase `CafeRecommender` permite recomendar cafeterías mediante los cuatro modos predefinidos o una petición libre.

En el modo libre, se combinan:

- La relevancia de las reseñas recuperadas.
- La cantidad de evidencias seleccionadas.
- La valoración media de la cafetería, ponderada según su número de reseñas.

La puntuación final experimental combina:

- **70 %:** relevancia relativa de la búsqueda.
- **30 %:** valoración general ponderada.

Estos pesos son provisionales y no han sido optimizados mediante una evaluación formal del recomendador.

**La puntuación final es un valor de ranking, no una probabilidad de satisfacción.**

---

## 6. Inteligencia Artificial Generativa: NVIDIA

El proyecto integra la API de **NVIDIA** mediante la librería `openai`, utilizando un endpoint compatible con OpenAI.

La integración está implementada en la clase `AIClient`, dentro de:

`starter/ia_client.py`

### Funcionalidades

**Análisis de reseñas**

NVIDIA puede analizar las siguientes características:

- Ruido.
- Ambiente.
- Bebidas.
- Comida.
- Precio.
- Comodidad.
- Atención.

Para cada característica devuelve una etiqueta: `positivo`, `negativo`, `neutro` o `no_mencionado`.

**Interpretación de preferencias**

En el modo libre, NVIDIA identifica preferencias como tranquilidad, estudiar o trabajar, wifi, matcha y brunch.

El sistema conserva también el texto original del usuario para realizar la búsqueda de reseñas.

**Explicación de recomendaciones**

NVIDIA genera una explicación breve para cada cafetería utilizando la reseña real recuperada.

El objetivo es explicar qué información respalda la recomendación y qué características no se pueden confirmar.

Por ejemplo:

> Federal Cafe podría encajar porque una reseña menciona un buen ambiente para trabajar o estudiar con el ordenador. No tenemos información suficiente para confirmar que sea un lugar tranquilo.

### Modos de funcionamiento

El cliente de NVIDIA dispone de dos modos.

| Modo | Funcionamiento |
|---|---|
| `mock` | Simula las respuestas sin realizar llamadas a la API. |
| `real` | Realiza llamadas a NVIDIA para interpretar preferencias, analizar reseñas y generar explicaciones. |

**El modo `real` es el que utiliza IA generativa de forma efectiva.** Se ha comprobado su funcionamiento mediante llamadas reales a NVIDIA.

El modo `mock` se utiliza para desarrollo, pruebas automáticas y demostraciones sin necesidad de una clave de API.

---

## 7. Estructura del proyecto

```text
Proyecto_ii/
│
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
│   └── review_summary.py
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
├── outputs/
│   └── metrics.json
│
├── models/
│
├── .gitignore
├── .env.example
├── requirements.txt
├── README.md
└── AI_USAGE.md
```

Los archivos generados, los modelos entrenados y el dataset completo se mantienen localmente y no se incluyen en el repositorio.

---

## 8. Instalación

El proyecto utiliza Python, scikit-learn y la API de NVIDIA.

### 8.1. Crear un entorno virtual

Desde la carpeta `Proyecto_ii`:

```bash
uv venv
```

En Git Bash (Windows), activar el entorno:

```bash
source .venv/Scripts/activate
```

### 8.2. Instalar dependencias

```bash
uv pip install -r requirements.txt
```

Las principales librerías utilizadas son:

- `pandas`
- `numpy`
- `scikit-learn`
- `joblib`
- `openai`
- `python-dotenv`
- `pytest`

### 8.3. Configuración de NVIDIA

Para utilizar el modo real es necesario disponer de una clave de NVIDIA.

Crear un archivo `.env` a partir de `.env.example`:

```dotenv
MODO_IA=mock
NVIDIA_API_KEY=TU_CLAVE_AQUI
NVIDIA_MODEL=nvidia/nemotron-3.5-super-vl-120b-a12b
```

Para utilizar NVIDIA, cambiar `MODO_IA=mock` por `MODO_IA=real`.

**El archivo `.env` no debe subirse a GitHub**, ya que contiene la clave privada de la API.

---

## 9. Ejecución del proyecto

Los siguientes comandos deben ejecutarse desde la carpeta `Proyecto_ii`, con el entorno virtual activo.

### 9.1. Entrenar el modelo

Requiere el dataset completo en `data/cafeterias_limpias.csv`.

```bash
python -m starter.train
```

Este comando entrena el modelo, calcula las métricas y guarda el modelo, el vectorizador y los resultados.

### 9.2. Generar perfiles de cafeterías

```bash
python -m starter.profiles
```

Genera el archivo:

`outputs/perfiles_cafeterias.csv`

### 9.3. Ejecutar el pipeline

**Modo mock:**

```bash
MODO_IA=mock python -m starter.pipeline
```

**Modo real:**

```bash
MODO_IA=real python -m starter.pipeline
```

El pipeline carga y valida las reseñas, predice su sentimiento y analiza características mediante `AIClient`.

Para esta primera versión se selecciona una reseña por cafetería. En modo real, el pipeline limita el análisis a cinco reseñas para controlar las llamadas a NVIDIA.

Los resultados se guardan en:

- `outputs/resultados_pipeline_mock.csv`
- `outputs/resultados_pipeline_real.csv`

### 9.4. Ejecutar Café Match

**Modo mock:**

```bash
MODO_IA=mock python -m starter.recommender
```

**Modo real con NVIDIA:**

```bash
MODO_IA=real python -m starter.recommender
```

Al ejecutar el programa se puede seleccionar uno de los modos:

```text
CAFÉ MATCH

Modos: focus, social, trendy, surprise, libre
Elige un modo:
```

En el modo libre, el usuario introduce su petición en lenguaje natural.

El programa interpreta las preferencias, recupera las reseñas relevantes, genera un ranking y muestra una explicación para cada cafetería.

### Recomendación para la demostración real

Para la demostración con NVIDIA se recomienda utilizar **`top_n=3`** en la llamada a `recommend_from_text()` del método `main()`.

De esta forma se muestran tres cafeterías recomendadas y se evitan llamadas innecesarias a la API.

En la versión actual, cada explicación generada en modo real implica una llamada adicional a NVIDIA.

### Ejecución con el dataset de muestra

El recomendador permite ejecutarse directamente con los archivos incluidos en GitHub.

Al iniciarse, comprueba qué dataset está disponible:

- Si existe `data/cafeterias_limpias.csv`, utiliza las 103.082 reseñas originales.
- Si no existe, utiliza automáticamente `data/cafeterias_muestra.csv`, que contiene 300 reseñas.

Los perfiles se generan a partir del mismo dataset utilizado para buscar las recomendaciones. Por tanto, no es necesario generar previamente `outputs/perfiles_cafeterias.csv`.

Para ejecutar la demostración en modo simulado:

```bash
MODO_IA=mock python -m starter.recommender
```

Para utilizar NVIDIA real:

```bash
MODO_IA=real python -m starter.recommender
```

En el modo libre, el sistema interpreta las preferencias, busca reseñas y devuelve hasta tres cafeterías con sus explicaciones.

La demostración con la muestra se ha comprobado correctamente utilizando la petición:

*Quiero una cafetería tranquila para estudiar.*

La muestra ha sido seleccionada para incluir ejemplos de características relacionadas con los cuatro modos de recomendación. No constituye una muestra estadísticamente representativa del dataset completo y sus rankings pueden ser diferentes.
---

## 10. Tests

El proyecto utiliza `pytest` para comprobar el funcionamiento de los distintos componentes.

Se incluyen pruebas para:

- Predicción de sentimientos.
- Generación de perfiles.
- Búsqueda de reseñas.
- Cliente de NVIDIA en modo simulado.
- Recomendaciones personalizadas.
- Ejecución del pipeline.

Para ejecutar todos los tests:

```bash
python -m pytest -q
```

**Último resultado comprobado:**

```text
24 passed
```

Las pruebas utilizan datos pequeños y componentes simulados cuando corresponde, evitando llamadas reales a NVIDIA durante los tests automáticos.

Algunas pruebas también verifican la carga y predicción del modelo entrenado, por lo que requieren disponer de los archivos `joblib`.

---

## 11. Reproducibilidad

El proyecto utiliza una división de entrenamiento, validación y test reproducible mediante `random_state=42`.

El modelo y el vectorizador pueden regenerarse ejecutando el script de entrenamiento con el dataset completo.

El repositorio incluye una muestra de 300 reseñas para evitar subir archivos demasiado grandes.

Para reproducir los resultados completos del modelo, así como las recomendaciones basadas en las 103.082 reseñas, es necesario disponer de `data/cafeterias_limpias.csv`.

La muestra incluida no permite reproducir las métricas originales ni todos los rankings.

El modo `mock` permite probar la integración del código sin conexión con NVIDIA, mientras que el modo `real` requiere una clave de API válida.

---

## 12. Limitaciones y mejoras futuras

Aunque el sistema genera recomendaciones personalizadas, todavía presenta algunas limitaciones:

- TF-IDF utiliza coincidencias léxicas y no comprende todos los sinónimos o significados.
- Una reseña positiva en general puede contener comentarios negativos sobre alguna característica concreta.
- Las preferencias detectadas no se verifican todavía de forma individual para cada cafetería.
- La relevancia de las reseñas no garantiza que el establecimiento cumpla todos los requisitos del usuario.
- El ranking utiliza pesos experimentales que requieren una evaluación más completa.

Como continuación del proyecto, se plantea mejorar la evaluación del recomendador, ampliar el análisis de evidencias y desarrollar una interfaz interactiva para consultar las recomendaciones de forma más sencilla.

El objetivo es avanzar hacia un sistema de recomendación explicable, que combine Machine Learning, búsqueda de información e inteligencia artificial generativa utilizando datos reales.