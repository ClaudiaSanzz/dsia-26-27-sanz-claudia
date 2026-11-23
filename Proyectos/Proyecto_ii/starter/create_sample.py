import pandas as pd

from starter.loader import CafeLoader
from starter.profiles import CafeProfiles


def main():
    # Cargamos las reseñas completas
    reviews = CafeLoader().load_csv("data/cafeterias_limpias.csv")

    # Identificamos las características de cada reseña
    features = CafeProfiles().add_features(reviews)

    columnas = [
        "focus_tranquilo",
        "focus_trabajar",
        "social_ambiente",
        "social_grupos",
        "trending_matcha",
        "trending_brunch",
        "discovery_original",
        "discovery_escondido"
    ]

    # Seleccionamos reseñas que mencionan cada característica
    muestras = []

    for columna in columnas:
        seleccion = features[features[columna] > 0]

        cantidad = min(30, len(seleccion))

        muestras.append(
            seleccion.sample(n=cantidad, random_state=42)
        )

    # Unimos las reseñas seleccionadas y eliminamos duplicados
    muestra = pd.concat(muestras).drop_duplicates(subset=["reviewId"])

    # Completamos hasta 300 reseñas con ejemplos aleatorios
    if len(muestra) < 300:
        restantes = reviews[~reviews["reviewId"].isin(muestra["reviewId"])]

        adicionales = restantes.sample(
            n=300 - len(muestra),
            random_state=42
        )

        muestra = pd.concat([muestra, adicionales])

    # Conservamos únicamente las columnas originales
    muestra = muestra[reviews.columns]

    muestra.to_csv("data/cafeterias_muestra.csv", index=False)

    print("Reseñas de muestra:", len(muestra))
    print("Cafeterías:", muestra["itemId"].nunique())


if __name__ == "__main__":
    main()
