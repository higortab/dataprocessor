from dataclasses import dataclass

from .entidades import Aluno, Configuracao, Nota


@dataclass(frozen=True)
class ErroRegistro:
    arquivo: str
    linha: int
    mensagem: str


@dataclass(frozen=True)
class ResultadoProcessamento:
    alunos: tuple[Aluno, ...]
    notas: tuple[Nota, ...]
    erros: tuple[ErroRegistro, ...]
    configuracao: Configuracao
    medias_disciplina: dict[str, float]
    notas_invalidas: int

    def to_dict(self) -> dict:
        return {
            "resumo": {
                "alunos_processados": len(self.alunos),
                "notas_validas": len(self.notas),
                "notas_invalidas": self.notas_invalidas,
                "erros": len(self.erros),
            },
            "alunos": [
                {
                    "matricula": aluno.matricula,
                    "nome": aluno.nome,
                    "turma": aluno.turma,
                    "media": round(aluno.media(), 2),
                    "situacao": aluno.situacao(
                        self.configuracao.media_aprovacao,
                        self.configuracao.media_recuperacao,
                    ),
                }
                for aluno in self.alunos
            ],
            "medias_disciplina": {
                disciplina: round(media, 2)
                for disciplina, media in sorted(self.medias_disciplina.items())
            },
            "erros": [
                {"arquivo": erro.arquivo, "linha": erro.linha, "mensagem": erro.mensagem}
                for erro in self.erros
            ],
        }
