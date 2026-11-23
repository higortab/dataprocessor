import unittest

from painel.core.entidades import AlunoBruto, Configuracao, NotaBruta
from painel.services.processamento import executar_processamento


class ProcessamentoTestCase(unittest.TestCase):
    def test_calcula_media_do_aluno_e_da_disciplina(self):
        alunos = [
            AlunoBruto(2, "1001", "Ana Souza", "3A", "alunos.csv"),
            AlunoBruto(3, "1002", "Bruno Lima", "3B", "alunos.csv"),
        ]
        notas = [
            NotaBruta(2, "1001", "Matemática", "P1", "8.0", "notas.csv"),
            NotaBruta(3, "1001", "Português", "P1", "6.0", "notas.csv"),
            NotaBruta(4, "1002", "Matemática", "P1", "4.0", "notas.csv"),
            NotaBruta(5, "9999", "Matemática", "P1", "10", "notas.csv"),
        ]
        config = Configuracao(6.0, 4.0, 10.0)
        resultado = executar_processamento(alunos, notas, config)

        ana, bruno = resultado.alunos
        self.assertAlmostEqual(ana.media(), 7.0)
        self.assertEqual(ana.situacao(6.0, 4.0), "aprovado")
        self.assertEqual(bruno.situacao(6.0, 4.0), "recuperação")
        self.assertAlmostEqual(resultado.medias_disciplina["Matemática"], 6.0)
        self.assertEqual(resultado.notas_invalidas, 1)
        self.assertEqual(len(resultado.erros), 1)
        self.assertEqual(len(resultado.notas), 3)
