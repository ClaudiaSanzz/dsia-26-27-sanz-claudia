import pandas as pd

df = pd.read_csv("data/cafeterias_reviews_madrid.csv")

print("DIMENSIONES")
print(df.shape)

print("\nNULOS POR COLUMNA")
print(df.isna().sum().sort_values(ascending=False))

print("\nDUPLICADOS")
print("ReviewId duplicados:", df["reviewId"].duplicated().sum())
print("Número de reviews únicas:", df["reviewId"].nunique())
print("Número de cafeterías únicas:", df["itemId"].nunique())

print("\nRATING DE LAS REVIEWS")
print(df["rating_review"].value_counts().sort_index())

print("\nRATING DE LAS CAFETERÍAS")
print(df["rating_cafeteria"].value_counts().sort_index())

print("\nIDIOMAS")
print(df["language"].value_counts().head(20))

print("\nPRECIOS")
print(df["priceInterval"].value_counts(dropna=False))

print("\nFECHAS")
print("Fecha mínima:", df["fecha_review"].min())
print("Fecha máxima:", df["fecha_review"].max())

print("\nREVIEWS SIN TEXTO")
print(df["texto_review"].isna().sum())

print("\nREVIEWS SIN TÍTULO")
print(df["titulo_review"].isna().sum())

print("\nREVIEWS CON IMÁGENES")
print(df["images"].notna().sum())

print("\nEJEMPLO")
print(
    df[
        [
            "name",
            "rating_cafeteria",
            "priceInterval",
            "rating_review",
            "language",
            "fecha_review",
            "texto_review",
        ]
    ].head(10)
)