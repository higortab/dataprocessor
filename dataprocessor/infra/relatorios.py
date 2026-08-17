from abc import ABC, abstractmethod


class GeradorRelatorio(ABC):
    @abstractmethod
    def render(self, resultado) -> str:
        ...

class RelatorioTexto(GeradorRealatorio):
    def render(self, resultado) -> str:
        return "\n".join(
            [
                "=== DataProcessor CLI ===",
                f"Clientes válidos: {len(resultado.clientes)}",
                f"Transações válidas: {len(resultado.transacoes)}",
                f"Total aprovado: R$ {resultado.total_aprovado:.2f}",
            ]
        )

class RelatorioJson(GeradorRelatorio):
    def render(self, resultado) -> str:
        return json.dumps(resultado.to_dict(), ensure_ascii=False, indent=2) + 'n'

def criar_gerador(formato: str) -> GeradorRelatorio:
    geradores = {
        "texto": RelatorioTexto,
        "json": RelatorioJson
    }
    return geradores[formato]()