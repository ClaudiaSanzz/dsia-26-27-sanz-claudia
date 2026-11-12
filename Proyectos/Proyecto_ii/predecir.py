import joblib

# 1. Cargamos el modelo y el vectorizador ya entrenados
modelo = joblib.load("modelo_sentimiento.joblib")
vectorizador = joblib.load("vectorizador.joblib")


# 2. Función para predecir el sentimiento de una reseña
def predecir_sentimiento(texto):

    # Convertimos el texto en números
    X = vectorizador.transform([texto])

    # Hacemos la predicción
    prediccion = modelo.predict(X)

    return prediccion[0]


# 3. Probamos con una reseña nueva
if __name__ == "__main__":

    reseña = "Me encantó el café, el ambiente era muy agradable"

    resultado = predecir_sentimiento(reseña)

    print("Reseña:", reseña)
    print("Sentimiento predicho:", resultado)
