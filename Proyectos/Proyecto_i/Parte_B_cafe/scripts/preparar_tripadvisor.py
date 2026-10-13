import pandas as pd


# Cargar los datos originales
items = pd.read_pickle("data/Madrid/items.pkl")
reviews = pd.read_pickle("data/Madrid/reviews.pkl")


# Categorías que vamos a considerar relacionadas con cafeterías
categorias_cafe = {
    "Cafe",
    "Coffee & Tea",
    "Bakeries",
}


def es_cafeteria(tipos):
    if not isinstance(tipos, list):
        return False

    return any(tipo in categorias_cafe for tipo in tipos)


# Filtrar establecimientos
cafeterias = items[
    items["type"].apply(es_cafeteria)
].copy()


# Eliminar posibles establecimientos duplicados
cafeterias = cafeterias.drop_duplicates(subset="itemId")


# Cambiamos algunos nombres para que luego no haya confusión
cafeterias = cafeterias.rename(
    columns={
        "rating": "rating_cafeteria",
        "type": "categorias",
        "url": "url_cafeteria",
    }
)

reviews = reviews.rename(
    columns={
        "rating": "rating_review",
        "title": "titulo_review",
        "text": "texto_review",
        "date": "fecha_review",
        "url": "url_review",
    }
)


# Unir cafeterías con sus reviews mediante itemId
dataset = reviews.merge(
    cafeterias,
    on="itemId",
    how="inner"
)


# Convertimos la lista de categorías en texto
dataset["categorias"] = dataset["categorias"].apply(
    lambda x: ", ".join(x) if isinstance(x, list) else x
)


# Guardamos el dataset final
dataset.to_csv(
    "data/cafeterias_reviews_madrid.csv",
    index=False
)


print("Cafeterías únicas:", cafeterias["itemId"].nunique())
print("Reviews:", len(dataset))
print("Filas del dataset final:", len(dataset))
print("Columnas:", dataset.columns.tolist())

print("\nPrimeras filas:")
print(dataset.head())