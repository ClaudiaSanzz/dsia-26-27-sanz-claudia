
import pandas as pd


# 1. Cargamos los análisis realizados con NVIDIA
df = pd.read_csv("resultados_pipeline_real.csv")


# 2. Características que analiza NVIDIA
caracteristicas = [
    "ruido",
    "ambiente",
    "bebidas",
    "comida",
    "precio",
    "comodidad",
    "atencion"
]


# 3. Nos aseguramos de no contar dos veces la misma reseña
df = df.drop_duplicates(subset=["reviewId"])


# 4. Creamos una tabla con una fila por cafetería
resumen = df.groupby("itemId").agg(
    name=("name", "first"),
    resenas_analizadas=("reviewId", "count")
).reset_index()


# 5. Contamos las opiniones positivas y negativas
for caracteristica in caracteristicas:

    for sentimiento in ["positivo", "negativo"]:

        # Seleccionamos las reseñas con ese sentimiento
        opiniones = df[df[caracteristica] == sentimiento]

        # Contamos cuántas hay por cafetería
        conteo = opiniones.groupby("itemId").size()

        # Añadimos el resultado al resumen
        columna = caracteristica + "_" + sentimiento

        resumen[columna] = (
            resumen["itemId"]
            .map(conteo)
            .fillna(0)
            .astype(int)
        )


# 6. Guardamos el resumen
resumen.to_csv("resumen_opiniones.csv", index=False)


# 7. Mostramos los resultados
print("\nRESUMEN DE OPINIONES DE NVIDIA")
print("Reseñas analizadas:", len(df))
print("Cafeterías analizadas:", len(resumen))
print("\nResultados guardados en resumen_opiniones.csv")
