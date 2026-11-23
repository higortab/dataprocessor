import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from painel.main import main


class CliTestCase(unittest.TestCase):
    def test_cli_grava_relatorio_json_e_recria_a_pasta(self):
        with tempfile.TemporaryDirectory() as pasta:
            base = Path(pasta)
            (base / "alunos.csv").write_text(
                "matricula,nome,turma\n1001,  Ana Souza ,3A\n",
                encoding="utf-8",
            )
            (base / "notas.csv").write_text(
                "matricula,disciplina,avaliacao,nota\n"
                "1001, Matemática ,P1, 8.0 \n"
                "1001,Matemática,P2,4.0\n",
                encoding="utf-8",
            )
            (base / "config.json").write_text(
                '{"media_aprovacao": 6.0, "media_recuperacao": 4.0, "nota_maxima": 10.0}\n',
                encoding="utf-8",
            )
            saida = base / "output"
            with redirect_stdout(io.StringIO()):
                codigo = main(
                    [
                        "--alunos",
                        str(base / "alunos.csv"),
                        "--notas",
                        str(base / "notas.csv"),
                        "--config",
                        str(base / "config.json"),
                        "--formato",
                        "json",
                        "--output",
                        str(saida),
                    ]
                )

            self.assertEqual(codigo, 0)
            self.assertTrue((saida / "painel.log").is_file())
            dados = json.loads((saida / "relatorio.json").read_text(encoding="utf-8"))
            self.assertEqual(dados["alunos"][0]["nome"], "Ana Souza")
            self.assertEqual(dados["alunos"][0]["media"], 6.0)
            self.assertEqual(dados["alunos"][0]["situacao"], "aprovado")

    def test_arquivo_ausente_nao_derruba_o_programa(self):
        with tempfile.TemporaryDirectory() as pasta:
            with redirect_stdout(io.StringIO()):
                codigo = main(
                    [
                        "--alunos",
                        str(Path(pasta) / "ausente.csv"),
                        "--notas",
                        str(Path(pasta) / "ausente.csv"),
                        "--config",
                        str(Path(pasta) / "ausente.json"),
                        "--formato",
                        "texto",
                        "--output",
                        str(Path(pasta) / "output"),
                    ]
                )
        self.assertEqual(codigo, 1)
