import unittest
from pathlib import Path

from dataprocessor.config import AppConfig
from dataprocessor.services.processamento import executar_processamento

RAIZ = Path(__file__).resolve().parents[1]


class TestProcessamento(unittest.TestCase):
    def test_processamento_com_arquivos_oficiais(self):
        app_config = AppConfig(
            caminho_clientes=str(RAIZ / "data" / "clientes.csv"),
            caminho_transacoes=str(RAIZ / "data" / "transacoes.csv"),
            caminho_config=str(RAIZ / "data" / "config.json"),
        )
        resultado = executar_processamento(app_config)

        self.assertEqual(len(resultado["clientes"]), 2)
        self.assertEqual(len(resultado["clientes_invalidos"]), 3)
        self.assertEqual(len(resultado["transacoes"]), 2)
        self.assertEqual(len(resultado["transacoes_invalidas"]), 3)
        self.assertEqual(resultado["metricas"]["media_idade"], 39.5)
        self.assertEqual(resultado["metricas"]["total_aprovado"], 150.50)
        self.assertEqual(resultado["metricas"]["ticket_medio_aprovado"], 150.50)
