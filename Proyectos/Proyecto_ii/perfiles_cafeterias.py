
import pandas as pd


# 1. Cargamos todas las reseñas
df = pd.read_csv("cafeterias_limpias.csv")


# 2. Creamos un perfil por cafetería
perfiles = df.groupby("itemId").agg(
    name=("name", "first"),
    num_resenas=("rating_review", "count"),
    valoracion_media=("rating_review", "mean")
).reset_index()

# Convertimos la valoración a una escala de 1 a 5
perfiles["valoracion_media"] = (
    perfiles["valoracion_media"] / 10
).round(2)


# 3. Preparamos el texto de las reseñas
# Conservamos el texto original para mostrar ejemplos después
df["texto_review"] = df["texto_review"].fillna("")
texto = df["texto_review"].str.lower()


# 4. FOCUS MODE
# Primero identificamos las opiniones desfavorables

df["focus_ruidoso"] = texto.str.contains(
    r"mucho ruido|demasiado ruido|muy ruidos|"
    r"imposible concentrarse|nada tranquil|"
    r"no se puede concentrar|excesivamente ruidos",
    regex=True
)

df["focus_no_trabajar"] = texto.str.contains(
    r"no dejan trabajar|no permiten trabajar|"
    r"no se puede trabajar|no dejan estudiar|"
    r"no se puede estudiar|prohibido.*portátil|"
    r"prohibido.*portatil|no permiten.*portátil|"
    r"no permiten.*portatil|no hay wifi|"
    r"wifi no funciona|sin wifi|no hay enchufes|"
    r"sin enchufes|no dejan usar.*ordenador",
    regex=True
)

# Después buscamos señales favorables
df["focus_tranquilo"] = texto.str.contains(
    r"sitio tranquil|lugar tranquil|ambiente tranquil|"
    r"muy tranquil|bastante tranquil|sin ruido|"
    r"poco ruido|silencios|ideal para concentrarse|"
    r"perfecto para concentrarse|relajado y tranquil",
    regex=True
)

df["focus_trabajar"] = texto.str.contains(
    r"ideal para estudiar|perfecto para estudiar|"
    r"ideal para trabajar|perfecto para trabajar|"
    r"se puede estudiar|se puede trabajar|"
    r"pude estudiar|pude trabajar|"
    r"estuve estudiando|estuve trabajando|"
    r"teletrabajar|trabajar con el portátil|"
    r"trabajar con el portatil|estudiar con el portátil|"
    r"estudiar con el portatil|"
    r"buen wifi|wifi funciona|wifi gratis|"
    r"enchufes disponibles|hay enchufes|"
    r"mesas para trabajar|trabajar con ordenador",
    regex=True
)

# Si aparece una señal contraria, no la contamos como favorable
df["focus_tranquilo"] = (
    df["focus_tranquilo"] & ~df["focus_ruidoso"]
)

df["focus_trabajar"] = (
    df["focus_trabajar"] & ~df["focus_no_trabajar"]
)


# 5. SOCIAL MODE
df["social_mal_ambiente"] = texto.str.contains(
    r"mal ambiente|ambiente desagradable|"
    r"no se puede hablar|imposible conversar|"
    r"imposible charlar|ambiente incómodo",
    regex=True
)

df["social_no_grupos"] = texto.str.contains(
    r"no admiten grupos|no aceptan grupos|"
    r"no hay sitio para grupos|no cabíamos|"
    r"no cabiamos|no permiten grupos",
    regex=True
)

df["social_ambiente"] = texto.str.contains(
    r"buen ambiente|ambiente agradable|"
    r"ambiente acogedor|ambiente animado|"
    r"ideal para charlar|perfecto para charlar|"
    r"ideal para conversar|perfecto para conversar|"
    r"sitio acogedor|lugar acogedor",
    regex=True
)

df["social_grupos"] = texto.str.contains(
    r"ideal para grupos|perfecto para grupos|"
    r"para ir con amigos|con los amigos|"
    r"quedar con amigos|fuimos en grupo|"
    r"brunch delicioso|brunch buenísimo|"
    r"brunch buenisimo|ideal para brunch",
    regex=True
)

df["social_ambiente"] = (
    df["social_ambiente"] & ~df["social_mal_ambiente"]
)

df["social_grupos"] = (
    df["social_grupos"] & ~df["social_no_grupos"]
)


# 6. TRENDING MODE
# Aquí contamos menciones, no opiniones positivas
df["trending_matcha"] = texto.str.contains(
    r"matcha|flat white|cold brew|"
    r"café de especialidad|cafe de especialidad|"
    r"specialty coffee|chai latte",
    regex=True
)

df["trending_brunch"] = texto.str.contains(
    r"brunch|pancakes|tostadas francesas|"
    r"avocado toast|açaí|acai|"
    r"eggs benedict|huevos benedictinos",
    regex=True
)


# 7. DISCOVERY MODE
df["discovery_original"] = texto.str.contains(
    r"sitio original|lugar original|muy original|"
    r"decoración especial|decoracion especial|"
    r"sitio diferente|lugar diferente|"
    r"cafetería temática|cafeteria tematica|"
    r"decoración curiosa|decoracion curiosa|"
    r"experiencia diferente|concepto original",
    regex=True
)

df["discovery_escondido"] = texto.str.contains(
    r"joya escondida|rincón escondido|rincon escondido|"
    r"poco conocido|poco conocida|"
    r"lugar secreto|sitio escondido|"
    r"hidden gem|joya oculta",
    regex=True
)


# 8. Agrupamos las características
columnas = [
    "focus_tranquilo",
    "focus_ruidoso",
    "focus_trabajar",
    "focus_no_trabajar",
    "social_ambiente",
    "social_mal_ambiente",
    "social_grupos",
    "social_no_grupos",
    "trending_matcha",
    "trending_brunch",
    "discovery_original",
    "discovery_escondido"
]

# Contamos cuántas reseñas coinciden con cada característica
caracteristicas = df.groupby("itemId")[columnas].sum().reset_index()

# Incorporamos los recuentos a los perfiles
perfiles = perfiles.merge(
    caracteristicas,
    on="itemId",
    how="left"
)


# 9. Guardamos ejemplos reales de las reseñas
# Para cada característica guardamos una reseña de ejemplo
for columna in columnas:

    # Seleccionamos las reseñas que contienen esa característica
    ejemplos = df[df[columna]][
        ["itemId", "texto_review"]
    ].copy()

    # Nos quedamos con un ejemplo por cafetería
    ejemplos = ejemplos.drop_duplicates(subset=["itemId"])

    # Limitamos la longitud para que el CSV sea más fácil de leer
    ejemplos["texto_review"] = (
        ejemplos["texto_review"].str.slice(0, 220)
    )

    # Cambiamos el nombre de la columna
    ejemplos = ejemplos.rename(
        columns={"texto_review": "ejemplo_" + columna}
    )

    # Añadimos los ejemplos a los perfiles
    perfiles = perfiles.merge(
        ejemplos,
        on="itemId",
        how="left"
    )


# 10. Incorporamos los análisis de Gemini que ya tenemos
opiniones = pd.read_csv("resumen_opiniones.csv")

# Eliminamos el nombre duplicado
opiniones = opiniones.drop(columns=["name"])

perfiles = perfiles.merge(
    opiniones,
    on="itemId",
    how="left"
)


# 11. Guardamos los perfiles actualizados
perfiles.to_csv("perfiles_cafeterias.csv", index=False)


# 12. Mostramos los resultados
print("\nPERFILES DE CAFETERÍAS ACTUALIZADOS")

print("Total de cafeterías:", len(perfiles))
print("Total de reseñas:", len(df))

print("\nRESEÑAS CON COINCIDENCIAS POR CARACTERÍSTICA:")

for columna in columnas:
    print(columna, ":", df[columna].sum())

print("\nPerfiles guardados en perfiles_cafeterias.csv")
