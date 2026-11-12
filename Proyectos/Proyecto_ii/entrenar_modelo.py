
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score

from preparar_datos import preparar_datos


# 1. Cargamos los datos
df = preparar_datos("cafeterias_limpias.csv")

X = df["texto_review"]
y = df["sentimiento"]


# 2. Dividimos los datos: 60% train, 20% validation y 20% test
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.4, random_state=42, stratify=y
)

X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp
)


# 3. Convertimos los textos en números
vectorizador = TfidfVectorizer(max_features=10000)

X_train = vectorizador.fit_transform(X_train)
X_val = vectorizador.transform(X_val)
X_test = vectorizador.transform(X_test)


# 4. Creamos y entrenamos el modelo Random Forest
modelo = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

modelo.fit(X_train, y_train)


# 5. Evaluamos con validation
pred_val = modelo.predict(X_val)

print("\nVALIDATION")
print("Accuracy:", accuracy_score(y_val, pred_val))
print("F1-macro:", f1_score(y_val, pred_val, average="macro"))


# 6. Evaluamos con test
pred_test = modelo.predict(X_test)

print("\nTEST")
print("Accuracy:", accuracy_score(y_test, pred_test))
print("F1-macro:", f1_score(y_test, pred_test, average="macro"))


# 7. Guardamos el modelo y el vectorizador
joblib.dump(modelo, "modelo_sentimiento.joblib")
joblib.dump(vectorizador, "vectorizador.joblib")

print("\nModelo y vectorizador guardados correctamente")


# Modelo de clasificación de sentimiento:
# Utilizamos Random Forest para clasificar las reseñas
# como positivas, negativas o neutras.
# TF-IDF convierte los textos en números.
# Dividimos los datos en 60% train, 20% validation y 20% test.
