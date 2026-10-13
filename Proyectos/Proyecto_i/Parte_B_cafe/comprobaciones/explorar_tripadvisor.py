import pandas as pd

items = pd.read_pickle("data/Madrid/items.pkl")
reviews = pd.read_pickle("data/Madrid/reviews.pkl")

categorias_interes = {
    "Cafe",
    "Coffee & Tea",
    "Bakeries",
    "Dessert",
}

def es_cafe(tipos):
    if not isinstance(tipos, list):
        return False

    return any(tipo in categorias_interes for tipo in tipos)


cafeterias = items[
    items["type"].apply(es_cafe)
].copy()


print("TOTAL DE ESTABLECIMIENTOS DE MADRID:", len(items))

print("\nESTABLECIMIENTOS POR CATEGORÍA:")
for categoria in categorias_interes:
    cantidad = items["type"].apply(
        lambda tipos: isinstance(tipos, list) and categoria in tipos
    ).sum()

    print(f"{categoria}: {cantidad}")


print("\nESTABLECIMIENTOS ÚNICOS SELECCIONADOS:", len(cafeterias))
print("IDs únicos:", cafeterias["itemId"].nunique())


reviews_cafeterias = reviews[
    reviews["itemId"].isin(cafeterias["itemId"])
].copy()


print("\nREVIEWS DE ESTOS ESTABLECIMIENTOS:", len(reviews_cafeterias))

print("\nEJEMPLOS DE ESTABLECIMIENTOS:")
print(
    cafeterias[
        ["itemId", "name", "priceInterval", "rating", "type"]
    ].head(20)
)