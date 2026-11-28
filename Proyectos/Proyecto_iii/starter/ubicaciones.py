
"""Obtiene ubicaciones de cafeterías y las guarda en un CSV."""

import csv
import os
import time
import unicodedata
from pathlib import Path

import pandas as pd
import requests


RAIZ = Path(__file__).resolve().parents[1]
ENTRADA = RAIZ / "data" / "cafeterias_limpias.csv"
SALIDA = RAIZ / "data" / "cafeterias_ubicaciones.csv"

URL = "https://nominatim.openstreetmap.org/search"

COLUMNAS = [
    "itemId", "name", "direccion", "barrio",
    "distrito", "lat", "lon", "estado"
]


def normalizar(texto):
    """Normaliza nombres para comparar resultados."""

    texto = unicodedata.normalize("NFKD", str(texto))
    texto = "".join(
        letra for letra in texto
        if not unicodedata.combining(letra)
    )
    return " ".join(texto.lower().split())


def cargar_cafeterias():
    """Carga una única fila por cafetería."""

    ruta = ENTRADA

    if not ruta.exists():
        ruta = RAIZ / "data" / "cafeterias_muestra.csv"

    df = pd.read_csv(
        ruta,
        usecols=["itemId", "name"]
    )

    return df.drop_duplicates("itemId")


def cargar_procesadas():
    """Evita buscar dos veces la misma cafetería."""

    if not SALIDA.exists():
        return set()

    df = pd.read_csv(SALIDA)

    return set(df["itemId"].astype(str))


def buscar_ubicacion(nombre, sesion):
    """Busca posibles ubicaciones en Madrid."""

    respuesta = sesion.get(
        URL,
        params={
            "q": f"{nombre}, Madrid, España",
            "format": "jsonv2",
            "addressdetails": 1,
            "countrycodes": "es",
            "limit": 5
        },
        timeout=20
    )

    respuesta.raise_for_status()
    return respuesta.json()


def procesar_resultados(item_id, nombre, resultados):
    """Conserva una coincidencia candidata para revisión."""

    fila = {
        "itemId": item_id,
        "name": nombre,
        "direccion": "",
        "barrio": "",
        "distrito": "",
        "lat": "",
        "lon": "",
        "estado": "no_encontrado"
    }

    for lugar in resultados:

        direccion = lugar.get("address", {})
        nombre_lugar = lugar.get("name", "")

        # Comprobamos la ciudad
        ciudad = (
            direccion.get("city")
            or direccion.get("town")
            or direccion.get("municipality")
            or ""
        )

        if normalizar(ciudad) != "madrid":
            continue

        # No aceptamos automáticamente un local
        # con nombre diferente al de nuestro CSV.
        if normalizar(nombre_lugar) != normalizar(nombre):
            continue

        calle = direccion.get("road", "")
        numero = direccion.get("house_number", "")

        if calle:
            direccion_corta = f"{calle}, {numero}".strip(", ")
        else:
            direccion_corta = lugar.get("display_name", "")

        fila["direccion"] = direccion_corta
        fila["barrio"] = (
            direccion.get("neighbourhood")
            or direccion.get("quarter")
            or ""
        )
        fila["distrito"] = (
            direccion.get("city_district")
            or direccion.get("suburb")
            or ""
        )
        fila["lat"] = lugar.get("lat", "")
        fila["lon"] = lugar.get("lon", "")

        # Hay que revisar el establecimiento antes
        # de utilizarlo como ubicación confirmada.
        fila["estado"] = "revisar"
        break

    return fila


def guardar_resultado(fila):
    """Guarda cada cafetería sin perder resultados previos."""

    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    nuevo = not SALIDA.exists()

    with open(
        SALIDA,
        "a",
        encoding="utf-8",
        newline=""
    ) as archivo:

        escritor = csv.DictWriter(
            archivo,
            fieldnames=COLUMNAS
        )

        if nuevo:
            escritor.writeheader()

        escritor.writerow(fila)


def main():
    """Procesa un lote de cafeterías pendientes."""

    cafeterias = cargar_cafeterias()
    procesadas = cargar_procesadas()

    pendientes = cafeterias[
        ~cafeterias["itemId"].astype(str).isin(procesadas)
    ]

    # Empezamos con un lote pequeño de prueba.
    limite = 10
    pendientes = pendientes.head(limite)

    identificacion = os.getenv("COFI_USER_AGENT")

    if not identificacion:
        print(
            "Configura COFI_USER_AGENT con el nombre "
            "del proyecto y un contacto identificable."
        )
        return

    sesion = requests.Session()
    sesion.headers.update({
        "User-Agent": identificacion
    })

    print(f"Cafeterías pendientes en este lote: {len(pendientes)}")

    for indice, (_, cafe) in enumerate(pendientes.iterrows(), 1):

        item_id = cafe["itemId"]
        nombre = cafe["name"]

        print(f"\n[{indice}/{len(pendientes)}] {nombre}")

        try:
            resultados = buscar_ubicacion(nombre, sesion)

            fila = procesar_resultados(
                item_id,
                nombre,
                resultados
            )

            guardar_resultado(fila)

            print("Estado:", fila["estado"])
            print("Dirección:", fila["direccion"] or "No encontrada")

        except requests.RequestException as error:
            print("Error de conexión:", error)
            print("Detenemos el lote para evitar más peticiones.")
            break

        # Dejamos margen respecto al límite del servidor.
        time.sleep(2)

    print(f"\nResultados guardados en: {SALIDA}")


if __name__ == "__main__":
    main()
