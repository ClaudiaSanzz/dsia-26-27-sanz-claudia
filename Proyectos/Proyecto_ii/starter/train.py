
import json
from pathlib import Path

import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    classification_report,
    confusion_matrix
)

from starter.loader import CafeLoader
from starter.validator import CafeValidator
from starter.data_preparation import DataPreparation


class SentimentTrainer:

    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=10000)
        self.model = LogisticRegression(max_iter=1000)

    def split_data(self, data):
        # Dividimos en 60% train, 20% validación y 20% test
        X = data["texto_review"]
        y = data["sentimiento"]

        X_train, X_temp, y_train, y_temp = train_test_split(
            X, y, test_size=0.4, random_state=42, stratify=y
        )

        X_val, X_test, y_val, y_test = train_test_split(
            X_temp, y_temp, test_size=0.5,
            random_state=42, stratify=y_temp
        )

        return X_train, X_val, X_test, y_train, y_val, y_test

    def train(self, X_train, y_train):
        # Transformamos los textos y entrenamos
        X_train = self.vectorizer.fit_transform(X_train)
        self.model.fit(X_train, y_train)

    def evaluate(self, X, y):
        # Predecimos y calculamos las métricas
        X = self.vectorizer.transform(X)
        predictions = self.model.predict(X)

        return {
            "accuracy": accuracy_score(y, predictions),
            "f1_macro": f1_score(y, predictions, average="macro"),
            "classification_report": classification_report(
                y, predictions, output_dict=True, zero_division=0
            ),
            "classes": self.model.classes_.tolist(),
            "confusion_matrix": confusion_matrix(
                y, predictions, labels=self.model.classes_
            ).tolist()
        }

    def save(self):
        # Guardamos el modelo y el vectorizador
        Path("models").mkdir(exist_ok=True)

        joblib.dump(self.model, "models/model.joblib")
        joblib.dump(self.vectorizer, "models/vectorizer.joblib")

    def save_metrics(self, validation, test):
        # Guardamos las métricas en JSON
        metrics = {
            "validation": validation,
            "test": test
        }

        Path("outputs").mkdir(exist_ok=True)

        with open("outputs/metrics.json", "w", encoding="utf-8") as file:
            json.dump(metrics, file, indent=4, ensure_ascii=False)


def main():
    # Cargamos y validamos las reseñas
    loader = CafeLoader()
    validator = CafeValidator()

    reviews = loader.load_csv("data/cafeterias_limpias.csv")
    reviews = validator.validate_columns(reviews)
    reviews = validator.remove_empty_reviews(reviews)

    # Preparamos los datos
    preparation = DataPreparation()
    data = preparation.prepare(reviews)

    # Dividimos y entrenamos
    trainer = SentimentTrainer()

    X_train, X_val, X_test, y_train, y_val, y_test = trainer.split_data(data)

    trainer.train(X_train, y_train)

    # Evaluamos el modelo
    validation = trainer.evaluate(X_val, y_val)
    test = trainer.evaluate(X_test, y_test)

    print("Validation:")
    print("Accuracy:", round(validation["accuracy"], 4))
    print("F1 macro:", round(validation["f1_macro"], 4))

    print("\nTest:")
    print("Accuracy:", round(test["accuracy"], 4))
    print("F1 macro:", round(test["f1_macro"], 4))

    # Guardamos el modelo y las métricas
    trainer.save()
    trainer.save_metrics(validation, test)


if __name__ == "__main__":
    main()
