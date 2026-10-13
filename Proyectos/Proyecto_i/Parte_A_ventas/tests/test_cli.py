from ventas.cli import main


def test_cli_crea_archivo(tmp_path):
    """Comprueba que la CLI genera correctamente un archivo limpio."""

    ruta_entrada = tmp_path / "ventas.csv"
    ruta_salida = tmp_path / "ventas_limpias.csv"

    ruta_entrada.write_text(
        "fecha,region,producto,unidades,precio_unitario,cliente_id\n"
        "2026-01-09,Sur,Cable Kit,7,12.5,C005\n"
        "2026-01-10,Norte,Sensor A,-2,10.0,C006\n"
    )

    main(ruta_entrada, ruta_salida)

    assert ruta_salida.exists()

    contenido = ruta_salida.read_text()

    assert "importe" in contenido
    assert "C005" in contenido
    assert "C006" not in contenido