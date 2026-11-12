
import pandas as pd


# 1. Cargamos los perfiles de todas las cafeterías
df = pd.read_csv("perfiles_cafeterias.csv")

# Nos quedamos con cafeterías con al menos 10 reseñas
df = df[df["num_resenas"] >= 10].copy()


# 2. Calculamos la puntuación general
media_global = df["valoracion_media"].mean()

df["score_base"] = (
    (df["num_resenas"] * df["valoracion_media"] + 20 * media_global)
    / (df["num_resenas"] + 20)
) / 5 * 100


# 3. Mostramos los modos de Café Match
print("\nCAFÉ MATCH")
print("1. Focus Mode - Estudiar o trabajar")
print("2. Social Mode - Quedar con amigos")
print("3. Trending Mode - Sitios populares")
print("4. Discovery Mode - Descubrir sitios diferentes")

modo = input("\n¿Qué plan tienes? (1-4): ")


# 4. Preguntamos las preferencias según el modo
if modo == "1":

    print("\nFOCUS MODE")
    print("1. Quiero un sitio tranquilo")
    print("2. Quiero estudiar o trabajar con mi portátil")

    opcion = input("¿Qué necesitas? (1-2): ")

    if opcion == "1":
        positiva = "focus_tranquilo"
        negativa = "focus_ruidoso"
    elif opcion == "2":
        positiva = "focus_trabajar"
        negativa = "focus_no_trabajar"
    else:
        raise ValueError("Opción no válida")

elif modo == "2":

    print("\nSOCIAL MODE")
    print("1. Quiero un sitio agradable para charlar")
    print("2. Quiero quedar con amigos o hacer un brunch")

    opcion = input("¿Qué te apetece? (1-2): ")

    if opcion == "1":
        positiva = "social_ambiente"
        negativa = "social_mal_ambiente"
    elif opcion == "2":
        positiva = "social_grupos"
        negativa = "social_no_grupos"
    else:
        raise ValueError("Opción no válida")

elif modo == "3":

    print("\nTRENDING MODE")
    print("1. Matcha y café de especialidad")
    print("2. Brunch y desayunos especiales")

    opcion = input("¿Qué te interesa? (1-2): ")

    if opcion == "1":
        positiva = "trending_matcha"
    elif opcion == "2":
        positiva = "trending_brunch"
    else:
        raise ValueError("Opción no válida")

    negativa = None

elif modo == "4":

    print("\nDISCOVERY MODE")
    print("1. Cafeterías originales o diferentes")
    print("2. Rincones poco conocidos")

    opcion = input("¿Qué quieres descubrir? (1-2): ")

    if opcion == "1":
        positiva = "discovery_original"
    elif opcion == "2":
        positiva = "discovery_escondido"
    else:
        raise ValueError("Opción no válida")

    negativa = None

else:
    raise ValueError("Modo no válido")


# 5. Calculamos la puntuación personalizada
df["score"] = df["score_base"]

favorables = df[positiva].fillna(0)

if negativa is not None:

    desfavorables = df[negativa].fillna(0)

    # Combinamos las señales favorables y desfavorables
    ajuste = (
        (favorables - desfavorables)
        / (favorables + desfavorables + 5)
    ) * 15

    df["score"] += ajuste

    # Número de reseñas que contienen señales relacionadas
    df["evidencias"] = favorables + desfavorables

else:

    # Para Trending y Discovery contamos menciones temáticas
    ajuste = favorables / (favorables + 10) * 15

    df["score"] += ajuste
    df["evidencias"] = favorables


# 6. Ajustamos la puntuación según el modo
if modo == "3":

    # Favorecemos cafeterías históricamente populares
    df["score"] += (
        df["num_resenas"] / df["num_resenas"].max()
    ) * 5

elif modo == "4":

    # Favorecemos cafeterías menos conocidas
    df["score"] += (
        1 - df["num_resenas"] / df["num_resenas"].max()
    ) * 5


# 7. Separamos las cafeterías según la información disponible
con_evidencias = df[df["evidencias"] > 0].copy()

# Ordenamos primero según la evidencia de la preferencia
# y después según la valoración general

if negativa is not None:

    con_evidencias["compatibilidad"] = (
        favorables.loc[con_evidencias.index]
        - desfavorables.loc[con_evidencias.index]
    ) / (
        favorables.loc[con_evidencias.index]
        + desfavorables.loc[con_evidencias.index]
        + 5
    )

else:

    con_evidencias["compatibilidad"] = (
        favorables.loc[con_evidencias.index]
        / (favorables.loc[con_evidencias.index] + 10)
    )

con_evidencias = con_evidencias.sort_values(
    ["compatibilidad", "score_base"],
    ascending=False
)


# 9. Seleccionamos las columnas que queremos mostrar
columnas = [
    "name",
    "valoracion_media",
    "num_resenas",
    "evidencias",
    "score"
]


# 10. Mostramos las cafeterías con información relevante
print("\nCAFETERÍAS CON INFORMACIÓN SOBRE TU PREFERENCIA:")

if len(con_evidencias) > 0:

    print(
        con_evidencias[columnas]
        .head(5)
        .round(2)
        .to_string(index=False)
    )

else:
    print("No hemos encontrado cafeterías con información sobre esta preferencia.")


