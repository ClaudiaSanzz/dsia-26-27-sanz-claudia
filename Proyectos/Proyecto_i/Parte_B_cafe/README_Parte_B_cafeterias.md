# Proyecto I - Parte B: Cafeterías de Madrid

## Descripción

Esta parte del Proyecto I utiliza un dataset público de reseñas de TripAdvisor para analizar cafeterías de Madrid.

El objetivo es construir un pipeline en Python que permita:

- cargar los datos;
- validar su calidad;
- separar filas válidas e inválidas;
- calcular métricas sobre las cafeterías y sus reseñas;
- consultar los resultados desde línea de comandos mediante una CLI;
- comprobar el correcto funcionamiento del código mediante tests con `pytest`;
- comprobar la cobertura de los tests con `pytest-cov`.

El proyecto utiliza establecimientos relacionados con las siguientes categorías:

- `Cafe`
- `Coffee & Tea`
- `Bakeries`

A partir de estas categorías se seleccionan los establecimientos relacionados con cafeterías y se unen con sus correspondientes reseñas.

El dataset final utilizado por la aplicación contiene:

- 1.159 cafeterías filtradas inicialmente.
- 105.744 reseñas.
- 16 columnas.

Después de aplicar las reglas de validación quedan:

- 104.633 filas válidas.
- 1.111 filas inválidas.
- 1.016 cafeterías presentes en las filas válidas.

---

# Dataset

## Origen

El dataset original utilizado es:

**TripAdvisor Restaurant Reviews - Version 2.0.0**

Autores:

- Pablo Pérez-Núñez
- Eva Blanco
- Verónica Bolón-Canedo
- Beatriz Remeseiro

Publicado en Zenodo en enero de 2025.

URL de origen:

https://zenodo.org/records/14622324

DOI:

`10.5281/zenodo.14622324`

Los datos fueron recopilados en 2023.

Para este proyecto se utiliza únicamente el archivo correspondiente a Madrid.

## Licencia

El dataset está publicado bajo licencia:

**Creative Commons Attribution 4.0 International (CC BY 4.0).**

## Fecha de descarga

Fecha de descarga utilizada para este proyecto:

**4 de octubre de 2026.**

## Archivos originales

El archivo correspondiente a Madrid contiene tres datasets:

```text
items.pkl
reviews.pkl
users.pkl
```

### `items.pkl`

Contiene información de los establecimientos:

- `itemId`
- `name`
- `city`
- `priceInterval`
- `url`
- `rating`
- `type`

### `reviews.pkl`

Contiene información de las reseñas:

- `reviewId`
- `userId`
- `itemId`
- `title`
- `text`
- `date`
- `rating`
- `language`
- `images`
- `url`

### `users.pkl`

Contiene información anonimizada de usuarios. Este archivo no se utiliza actualmente en el pipeline.

---

# Exploración inicial del dataset

Antes de construir el pipeline se realizó una exploración de los establecimientos disponibles.

El dataset original de Madrid contiene:

```text
11.544 establecimientos
```

Las categorías relacionadas con el dominio del proyecto incluían:

```text
Cafe: 899
Coffee & Tea: 438
Bakeries: 132
Dessert: 192
```

Finalmente se decidió utilizar únicamente:

```text
Cafe
Coffee & Tea
Bakeries
```

La categoría `Dessert` no se incluyó porque puede contener establecimientos como heladerías, tiendas de dulces u otros negocios que no encajan directamente con el objetivo del proyecto.

Después del filtrado se obtuvieron:

```text
1.159 cafeterías
105.744 reviews
```

---

# Preparación de los datos

El dataset original no se utiliza directamente.

Para que el proceso sea reproducible se creó el script:

```text
scripts/preparar_tripadvisor.py
```

Este script realiza los siguientes pasos:

1. Carga `items.pkl`.
2. Carga `reviews.pkl`.
3. Selecciona establecimientos de las categorías `Cafe`, `Coffee & Tea` y `Bakeries`.
4. Elimina establecimientos duplicados mediante `itemId`.
5. Selecciona únicamente las reviews de esos establecimientos.
6. Une establecimientos y reviews utilizando `itemId`.
7. Renombra columnas para distinguir ratings y URLs de cafeterías y reviews.
8. Convierte las categorías a texto.
9. Genera el dataset final.

El resultado se guarda en:

```text
data/cafeterias_reviews_madrid.csv
```

Para volver a generarlo:

```bash
python scripts/preparar_tripadvisor.py
```

---

# Dataset final

El archivo:

```text
data/cafeterias_reviews_madrid.csv
```

contiene las siguientes columnas:

```text
reviewId
userId
itemId
titulo_review
texto_review
fecha_review
rating_review
language
images
url_review
name
city
priceInterval
url_cafeteria
rating_cafeteria
categorias
```

Cada fila representa una review.

Por tanto, una misma cafetería puede aparecer en varias filas, una por cada reseña asociada.

---

# Calidad de los datos

Durante la exploración del dataset final se encontraron los siguientes aspectos.

## Valores nulos

```text
priceInterval: 2116
titulo_review: 1
```

## Duplicados

Se encontraron:

```text
555 reviewId duplicados
```

## Ratings de las reviews

Las puntuaciones toman los valores:

```text
10
20
30
40
50
```

equivalentes a 1, 2, 3, 4 y 5 estrellas.

## Ratings de cafeterías

Se detectó un valor anómalo:

```text
rating_cafeteria = -10
```

que se considera inválido durante la validación.

## Idiomas

Los idiomas más frecuentes son:

```text
es
en
it
fr
pt
de
```

El español es el idioma más frecuente.

## Fechas

Las reviews abarcan aproximadamente desde:

```text
2007-08-06
```

hasta:

```text
2023-06-10
```

---

# Estructura del proyecto

```text
Parte_B_cafe/
│
├── cafeterias/
│   ├── __init__.py
│   ├── loader.py
│   ├── validator.py
│   ├── metrics.py
│   └── cli.py
│
├── data/
│   ├── Madrid/
│   │   ├── items.pkl
│   │   ├── reviews.pkl
│   │   └── users.pkl
│   └── cafeterias_reviews_madrid.csv
│
├── scripts/
│   └── preparar_tripadvisor.py
│
├── tests/
│   ├── test_loader.py
│   ├── test_validator.py
│   ├── test_metrics.py
│   └── test_cli.py
│
├── pytest.ini
├── requirements.txt
└── README.md
```

---

# Instalación

Las dependencias necesarias se encuentran en `requirements.txt`.

```text
pandas
pytest
pytest-cov
```

Para instalarlas:

```bash
pip install -r requirements.txt
```

---

# Carga de datos

El módulo `cafeterias/loader.py` carga el dataset y devuelve un `DataFrame`.

Si el archivo no existe o no puede cargarse correctamente, se lanza:

```text
CafeDataLoadError
```

---

# Validación

El módulo `cafeterias/validator.py` comprueba la calidad de cada fila.

Una fila se considera válida cuando:

- `reviewId` no es nulo;
- `itemId` no es nulo;
- `name` no está vacío;
- `texto_review` no está vacío;
- `rating_review` está entre 10 y 50;
- `rating_cafeteria` está entre 10 y 50;
- `fecha_review` puede convertirse correctamente a fecha;
- `reviewId` no está duplicado.

Los campos `priceInterval` y `titulo_review` pueden ser nulos sin invalidar la fila.

Resultados actuales:

```text
Filas totales: 105744
Filas válidas: 104633
Filas inválidas: 1111
```

---

# Métricas

El módulo `cafeterias/metrics.py` calcula cuatro métricas sobre las filas válidas:

## Cafeterías con más reviews

```bash
python -m cafeterias.cli popular
```

## Cafeterías mejor valoradas

Exige por defecto un mínimo de 20 reviews.

```bash
python -m cafeterias.cli top
```

## Porcentaje de reviews positivas

Se considera positiva una review con puntuación 40 o 50.

```bash
python -m cafeterias.cli positivas
```

## Distribución de ratings

```bash
python -m cafeterias.cli ratings
```

---

# CLI

La aplicación se ejecuta con:

```bash
python -m cafeterias.cli ACCION
```

## Resumen

```bash
python -m cafeterias.cli summary
```

Resultado actual:

```text
RESUMEN DEL DATASET
Filas totales: 105744
Filas válidas: 104633
Filas inválidas: 1111
Cafeterías: 1016
Reviews: 104633
```

## Cafeterías con más reviews

```bash
python -m cafeterias.cli popular
```

## Cafeterías mejor valoradas

```bash
python -m cafeterias.cli top
```

## Reviews positivas

```bash
python -m cafeterias.cli positivas
```

## Distribución de puntuaciones

```bash
python -m cafeterias.cli ratings
```

También se puede indicar otro dataset:

```bash
python -m cafeterias.cli summary --data ruta/al/archivo.csv
```

---

# Tests

Los tests están implementados con `pytest`.

Se incluyen tests para:

- `loader`
- `validator`
- `metrics`
- `cli`

Actualmente existen:

```text
10 tests
```

Para ejecutarlos:

```bash
python -m pytest -q
```

Resultado actual:

```text
10 passed
```

---

# Test de integración

Existe un test marcado como:

```python
@pytest.mark.integration
```

Este test utiliza el dataset real y comprueba:

- que puede cargarse;
- que contiene más de 10.000 filas;
- que contiene las columnas principales esperadas.

La marca está registrada en `pytest.ini`:

```ini
[pytest]
markers =
    integration: tests de integración que utilizan el dataset real
```

Para excluir los tests de integración:

```bash
python -m pytest -q -m "not integration"
```

Resultado actual:

```text
9 passed, 1 deselected
```

---

# Cobertura

La cobertura se calcula con `pytest-cov`.

```bash
python -m pytest --cov=cafeterias --cov-report=term-missing --cov-fail-under=60
```

Resultado actual:

```text
loader.py       85 %
validator.py    78 %
metrics.py     100 %
cli.py          53 %

TOTAL           72.92 %
```

El mínimo exigido es del 60 %, por lo que actualmente se supera el requisito.

---

# Integración continua

La integración continua se realizará mediante GitHub Actions.

El workflow deberá:

1. instalar Python;
2. instalar las dependencias;
3. ejecutar los tests;
4. comprobar que la cobertura es igual o superior al 60 %.

El comando será:

```bash
python -m pytest --cov=cafeterias --cov-report=term-missing --cov-fail-under=60
```

Cuando el workflow esté configurado y aparezca en verde en GitHub Actions, esta sección se actualizará con la evidencia correspondiente.

---

# Autora

Claudia Sanz Sainz-Rozas
