
## Modelo de Machine Learning

Para clasificar el sentimiento de las reseñas de las cafeterías se ha utilizado un modelo **RandomForestClassifier** de scikit-learn.

El dataset contiene **103.082 reseñas**, clasificadas en tres categorías a partir de sus valoraciones:

- **Positivo:** 73.873 reseñas.
- **Negativo:** 16.672 reseñas.
- **Neutro:** 12.537 reseñas.

### Preparación y entrenamiento

Los textos de las reseñas se han convertido en características numéricas utilizando **TF-IDF**, con un máximo de 10.000 características.

Los datos se han dividido en tres conjuntos:

- **60 % entrenamiento:** para entrenar el modelo.
- **20 % validación:** para evaluar su rendimiento.
- **20 % test:** para comprobar su rendimiento final.

Se ha utilizado `RandomForestClassifier` con 100 árboles y `random_state=42` para garantizar la reproducibilidad.

### Resultados

Las métricas obtenidas han sido:

| Métrica | Validación | Test |
|---|---|---|
| Accuracy | 0.8015 | 0.8002 |
| F1-macro | 0.5242 | 0.5206 |

El modelo obtiene aproximadamente un **80 % de accuracy** tanto en validación como en test. Sin embargo, el F1-macro es menor, lo que indica que el rendimiento no es igual para las tres clases.

Esto puede deberse, en parte, al desequilibrio del dataset, ya que las reseñas positivas son mucho más numerosas que las negativas y neutras.

### Guardado del modelo

Una vez entrenado, el modelo y el vectorizador TF-IDF se guardan utilizando `joblib`:

- `modelo_sentimiento.joblib`: modelo Random Forest entrenado.
- `vectorizador.joblib`: vectorizador TF-IDF.

Estos archivos permiten realizar nuevas predicciones sin tener que volver a entrenar el modelo.

### Ejecución

Para entrenar el modelo y obtener las métricas:

```bash
uv run entrenar_modelo.py
```

Para ejecutar el pipeline de Café Match:

```bash
uv run pipeline.py
```

El pipeline utiliza el modelo entrenado para clasificar el sentimiento de las reseñas y permite analizar sus características mediante Gemini en modo `mock` o `real`.
