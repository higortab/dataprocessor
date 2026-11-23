import json
import unittest

from painel.core.entidades import Aluno, Configuracao, Nota
from painel.core.resultados import ErroRegistro, ResultadoProcessamento
from painel.infra.relatorios import RelatorioJson, RelatorioTexto, criar_gerador


class RelatoriosTestCase(unittest.TestCase):
    def setUp(self):
        self.resultado = ResultadoProcessamento(
            alunos=(Aluno("1001", "Ana Souza", "3A", (8.0, 6.0)),),
            notas=(
                Nota("1001", "Matemática", "P1", 8.0),
                Nota("1001", "Português", "P1", 6.0),
            ),
            erros=(ErroRegistro("notas.csv", 3, "matrícula inexistente (1033)"),),
            configuracao=Configuracao(6.0, 4.0, 10.0),
            medias_disciplina={"Português": 6.0, "Matemática": 8.0},
            notas_invalidas=1,
        )

    def test_texto_e_json_usam_o_mesmo_resultado(self):
        texto = RelatorioTexto().render(self.resultado)
        dados = json.loads(RelatorioJson().render(self.resultado))

        self.assertIn("Alunos processados: 1", texto)
        self.assertIn("Ana Souza", texto)
        self.assertIn("média 7.00  aprovado", texto)
        self.assertNotIn("Física", texto)
        self.assertIn("Matemática", texto)
        self.assertIn("notas.csv:3  matrícula inexistente (1033)", texto)
        self.assertEqual(dados["resumo"]["notas_validas"], 2)
        self.assertEqual(dados["alunos"][0]["situacao"], "aprovado")
        self.assertEqual(dados["alunos"][0]["media"], 7.0)
        self.assertEqual(list(dados["medias_disciplina"]), ["Matemática", "Português"])

    def test_fabrica_devolve_geradores_diferentes(self):
        self.assertIsInstance(criar_gerador("texto"), RelatorioTexto)
        self.assertIsInstance(criar_gerador("json"), RelatorioJson)
        self.assertNotEqual(
            criar_gerador("texto").render(self.resultado)[:1],
            criar_gerador("json").render(self.resultado)[:1],
        )
