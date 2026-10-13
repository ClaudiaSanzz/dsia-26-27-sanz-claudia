"""Contrato de los datos de ventas."""

from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Venta(BaseModel):
    """Representa una venta válida."""

    model_config = ConfigDict(extra="forbid")

    fecha: date
    region: Literal["Norte", "Sur", "Este", "Oeste"]
    producto: str = Field(min_length=1)
    unidades: float = Field(gt=0)
    precio_unitario: float = Field(gt=0)
    cliente_id: str = Field(min_length=1)