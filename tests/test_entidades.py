import unittest

from painel.core.entidades import Aluno


class EntidadesTestCase(unittest.TestCase):
    def test_media_e_a_media_aritmetica_das_notas(self):
        aluno = Aluno("1001", "Ana Souza", "3A", (8.5, 7.0, 9.0))
        self.assertAlmostEqual(aluno.media(), 8.166666666666666)

    def test_situacao_usa_a_media_sem_arredondar(self):
        limites = (6.0, 4.0)
        self.assertEqual(Aluno("1", "A", "3A", (6.0,)).situacao(*limites), "aprovado")
        self.assertEqual(Aluno("2", "B", "3A", (5.999,)).situacao(*limites), "recuperação")
        self.assertEqual(Aluno("3", "C", "3A", (4.0,)).situacao(*limites), "recuperação")
        self.assertEqual(Aluno("4", "D", "3A", (3.999,)).situacao(*limites), "reprovado")

    def test_aluno_sem_notas_tem_media_zero(self):
        aluno = Aluno("1001", "Ana Souza", "3A")
        self.assertEqual(aluno.media(), 0.0)
        self.assertEqual(aluno.situacao(6.0, 4.0), "reprovado")
