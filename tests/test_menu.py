import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from dataprocessor.interfaces.menu import processar_caminhos


class ProcessarCaminhosTestCase(unittest.TestCase):
    def test_processa_dataset_padrao(self):
        resultado = processar_caminhos(
            "data/clientes.csv",
            "data/transacoes.csv",
            "data/config.json",
        )
        self.assertEqual(resultado.total_aprovado, 150.50)

    def test_mesmo_total_aprovado_que_a_cli(self):
        projeto = Path(__file__).resolve().parents[1]
        resultado = processar_caminhos(
            str(projeto / "data/clientes.csv"),
            str(projeto / "data/transacoes.csv"),
            str(projeto / "data/config.json"),
        )

        with tempfile.TemporaryDirectory() as pasta:
            saida = Path(pasta)
            processo = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "dataprocessor",
                    "--clientes",
                    str(projeto / "data/clientes.csv"),
                    "--transacoes",
                    str(projeto / "data/transacoes.csv"),
                    "--config",
                    str(projeto / "data/config.json"),
                    "--formato",
                    "json",
                    "--output",
                    str(saida),
                ],
                cwd=projeto,
                capture_output=True,
                text=True,
            )
            self.assertEqual(processo.returncode, 0, processo.stderr)
            relatorio = json.loads((saida / "relatorio.json").read_text(encoding="utf-8"))
            self.assertEqual(resultado.total_aprovado, relatorio["metricas"]["total_aprovado"])


if __name__ == "__main__":
    unittest.main()
