"""Contrato de los datos de reseñas de cafeterías."""

from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ReviewCafe(BaseModel):
    """Representa una reseña válida de una cafetería."""

    # No permitimos columnas extra que no estén definidas en el contrato
    model_config = ConfigDict(extra="forbid")

    # Identificador único de la reseña.
    # Debe ser un número positivo.
    reviewId: int = Field(gt=0)

    # Identificador del usuario.
    # Es obligatorio y no puede estar vacío.
    userId: str = Field(min_length=1)

    # Identificador de la cafetería.
    # Debe ser un número positivo.
    itemId: int = Field(gt=0)

    # Título de la reseña.
    # Lo consideramos obligatorio porque no queremos conservar filas con nulos.
    titulo_review: str = Field(min_length=1)

    # Texto principal de la reseña.
    # Es obligatorio y no puede estar vacío.
    texto_review: str = Field(min_length=1)

    # La fecha debe tener un formato válido.
    fecha_review: date

    # Escala de valoración utilizada en el dataset.
    rating_review: Literal[10, 20, 30, 40, 50]

    # Idioma de la reseña.
    # Debe estar informado.
    language: str = Field(min_length=1)

    # Información sobre imágenes.
    # También la consideramos obligatoria para evitar nulos.
    images: str = Field(min_length=1)

    # URL de la reseña original.
    url_review: str = Field(min_length=1)

    # Nombre de la cafetería.
    name: str = Field(min_length=1)

    # El dataset está formado por cafeterías de Madrid.
    city: Literal["Madrid"]

    # Rango de precio.
    # Lo consideramos obligatorio porque es importante para el análisis.
    priceInterval: str = Field(min_length=1)

    # URL de la cafetería.
    url_cafeteria: str = Field(min_length=1)

    # Valoración general de la cafetería.
    # La escala válida está entre 10 y 50.
    rating_cafeteria: int = Field(ge=10, le=50)

    # Categoría o categorías del establecimiento.
    categorias: str = Field(min_length=1)