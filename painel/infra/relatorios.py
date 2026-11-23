from abc import ABC, abstractmethod
import json

from ..core.resultados import ResultadoProcessamento


class GeradorRelatorio(ABC):
    @abstractmethod
    def render(self, resultado: ResultadoProcessamento) -> str: ...


class RelatorioTexto(GeradorRelatorio):
    def render(self, resultado: ResultadoProcessamento) -> str:
        config = resultado.configuracao
        linhas = [
            "PAINEL DE NOTAS — RESUMO",
            "",
            f"Alunos processados: {len(resultado.alunos)}",
            f"Registros de nota válidos: {len(resultado.notas)} | inválidos: {resultado.notas_invalidas}",
            "",
            "Situação dos alunos",
        ]
        for aluno in resultado.alunos:
            situacao = aluno.situacao(config.media_aprovacao, config.media_recuperacao)
            linhas.append(
                f"  {aluno.nome:<24} {aluno.turma:<2}  média {aluno.media():.2f}  {situacao}"
            )
        linhas.extend(["", "Média por disciplina"])
        for disciplina, media in sorted(resultado.medias_disciplina.items()):
            linhas.append(f"  {disciplina:<12} {media:.2f}")
        linhas.extend(["", f"Erros encontrados ({len(resultado.erros)})"])
        for erro in resultado.erros:
            linhas.append(f"  {erro.arquivo}:{erro.linha}  {erro.mensagem}")
        linhas.append("")
        return "\n".join(linhas)


class RelatorioJson(GeradorRelatorio):
    def render(self, resultado: ResultadoProcessamento) -> str:
        return json.dumps(resultado.to_dict(), ensure_ascii=False, indent=2) + "\n"


def criar_gerador(formato: str) -> GeradorRelatorio:
    geradores = {
        "texto": RelatorioTexto,
        "json": RelatorioJson,
    }
    return geradores[formato]()
