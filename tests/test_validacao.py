import unittest

from painel.core.entidades import AlunoBruto, NotaBruta
from painel.core.validador import validar_alunos, validar_notas


class ValidacaoTestCase(unittest.TestCase):
    def test_aluno_duplicado_preserva_o_primeiro_registro(self):
        registros = [
            AlunoBruto(2, "1001", "Ana Souza", "3A", "alunos.csv"),
            AlunoBruto(3, "1004", "Daniel Rocha", "3A", "alunos.csv"),
            AlunoBruto(4, "1004", "Daniel Rocha Filho", "3B", "alunos.csv"),
            AlunoBruto(5, "1050", "", "3A", "alunos.csv"),
            AlunoBruto(6, "10x7", "Bianca Torres", "3C", "alunos.csv"),
        ]
        validos, erros = validar_alunos(registros)
        self.assertEqual([aluno.nome for aluno in validos], ["Ana Souza", "Daniel Rocha"])
        self.assertEqual([(erro.linha, erro.mensagem) for erro in erros], [
            (4, "matrícula 1004 já cadastrada"),
            (5, "campo obrigatório vazio"),
            (6, "matrícula inválida ('10x7')"),
        ])

    def test_campo_vazio_tem_prioridade_sobre_nota_invalida(self):
        registros = [
            NotaBruta(2, "", "Matemática", "P1", "oito", "notas.csv"),
        ]
        validas, erros = validar_notas(registros, {"1001"}, 10.0)
        self.assertEqual(validas, [])
        self.assertEqual(erros[0].mensagem, "campo obrigatório vazio")

    def test_notas_acumulam_erros_sem_descartar_as_validas(self):
        registros = [
            NotaBruta(2, "1001", "Matemática", "P1", "8.5", "notas.csv"),
            NotaBruta(3, "1001", "Matemática", "P2", "--", "notas.csv"),
            NotaBruta(4, "1001", "Física", "P1", "12", "notas.csv"),
            NotaBruta(5, "1033", "Português", "P1", "4.7", "notas.csv"),
            NotaBruta(6, "1001", "Matemática", "P1", "9.0", "notas.csv"),
            NotaBruta(7, "1001", "História", "T1", "7.5", "notas.csv"),
        ]
        validas, erros = validar_notas(registros, {"1001"}, 10.0)
        self.assertEqual([nota.valor for nota in validas], [8.5, 7.5])
        self.assertEqual([erro.linha for erro in erros], [3, 4, 5, 6])
        self.assertIn("nota inválida ('--')", erros[0].mensagem)
        self.assertIn("fora do intervalo", erros[1].mensagem)
        self.assertIn("matrícula inexistente (1033)", erros[2].mensagem)
        self.assertIn("avaliação já lançada", erros[3].mensagem)
