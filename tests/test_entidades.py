import unittest
from dataclasses import FrozenInstanceError, replace

from dataprocessor.core.entidades import Cliente, Transacao
from dataprocessor.core.transformador import transformar_cliente


class TestEntidades(unittest.TestCase):
    def test_cliente_exibe_identificacao_derivada(self):
        cliente = Cliente(5, "Pedro Santos", "", 38, "Sao Paulo", "2023-02-30")
        self.assertEqual(cliente.identificacao, "#5 Pedro Santos")

    def test_transacao_esta_aprovada(self):
        aprovada = Transacao(1, 1, 150.50, "eletronicos", "2023-05-10", "aprovado")
        recusada = Transacao(4, 1, 300.00, "eletronicos", "2023-05-13", "recusado")
        self.assertTrue(aprovada.esta_aprovada)
        self.assertFalse(recusada.esta_aprovada)

    def test_transacao_resumo(self):
        transacao = Transacao(1, 1, 150.50, "eletronicos", "2023-05-10", "aprovado")
        self.assertEqual(transacao.resumo, "#1 R$ 150.50 aprovado")

    def test_cliente_eh_imutavel(self):
        cliente = Cliente(1, "João Silva", "joao.silva@email.com", 34, "Joinville", "2023-01-10")
        with self.assertRaises(FrozenInstanceError):
            cliente.nome = "Outro Nome"

    def test_transformar_cliente_nao_muta_original(self):
        original = Cliente(7, "  ana LIMA ", "ANA@Email.COM", 45, " Joinville ", "2023-01-25")
        normalizado = transformar_cliente(original)
        self.assertEqual(original.nome, "  ana LIMA ")
        self.assertEqual(normalizado.nome, "Ana Lima")
        self.assertEqual(normalizado.email, "ana@email.com")
        self.assertEqual(normalizado.cidade, "Joinville")
        self.assertIsNot(original, normalizado)

    def test_replace_cria_nova_entidade(self):
        cliente = Cliente(1, "João Silva", "joao.silva@email.com", 34, "Joinville", "2023-01-10")
        outro = replace(cliente, nome="João")
        self.assertEqual(cliente.nome, "João Silva")
        self.assertEqual(outro.nome, "João")
