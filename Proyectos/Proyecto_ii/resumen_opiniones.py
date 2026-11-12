
import pandas as pd


# 1. Cargamos los análisis de Gemini
df = pd.read_csv("analisis_resenas.csv")


# 2. Características que hemos analizado
caracteristicas = [
    "ruido", "ambiente", "bebidas", "comida",
    "precio", "comodidad", "atencion"
]


# 3. Creamos una tabla con una fila por cafetería
resumen = df.groupby("itemId").agg(
    name=("name", "first"),
    resenas_analizadas=("reviewId", "count")
).reset_index()


# 4. Contamos las opiniones positivas y negativas
for caracteristica in caracteristicas:

    for sentimiento in ["positivo", "negativo"]:

        # Contamos las reseñas con ese sentimiento
        conteo = df[df[caracteristica] == sentimiento].groupby(
            "itemId"
        ).size()

        # Añadimos el resultado al resumen
        columna = caracteristica + "_" + sentimiento
        resumen[columna] = resumen["itemId"].map(conteo).fillna(0).astype(int)


# 5. Guardamos los resultados
resumen.to_csv("resumen_opiniones.csv", index=False)


# 6. Mostramos el resultado
print(resumen.to_string(index=False))
print("\nCafeterías analizadas:", len(resumen))

