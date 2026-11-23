from dataclasses import dataclass


@dataclass(frozen=True)
class Configuracao:
    media_aprovacao: float
    media_recuperacao: float
    nota_maxima: float


@dataclass(frozen=True)
class AlunoBruto:
    linha: int
    matricula: str
    nome: str
    turma: str
    origem: str


@dataclass(frozen=True)
class NotaBruta:
    linha: int
    matricula: str
    disciplina: str
    avaliacao: str
    nota: str
    origem: str


@dataclass(frozen=True)
class Nota:
    matricula: str
    disciplina: str
    avaliacao: str
    valor: float


@dataclass(frozen=True)
class Aluno:
    matricula: str
    nome: str
    turma: str
    notas: tuple[float, ...] = ()

    def media(self) -> float:
        if not self.notas:
            return 0.0
        return sum(self.notas) / len(self.notas)

    def situacao(self, media_aprovacao: float, media_recuperacao: float) -> str:
        valor = self.media()
        if valor >= media_aprovacao:
            return "aprovado"
        if valor >= media_recuperacao:
            return "recuperação"
        return "reprovado"
