
from pathlib import Path

import pandas as pd

class CafeLoader:

    def load_csv(self, path):
        # Comprobamos que existe el archivo
        if not Path(path).exists():
            raise FileNotFoundError(f"No existe el archivo: {path}")

        # Cargamos los datos
        return pd.read_csv(path)
