import csv
import json
from pathlib import Path

from ..core.entidades import AlunoBruto, Configuracao, NotaBruta


def carregar_alunos(caminho: str | Path) -> list[AlunoBruto]:
    caminho = Path(caminho)
    with caminho.open(encoding="utf-8", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)
        return [
            AlunoBruto(
                linha=numero,
                matricula=(linha.get("matricula") or "").strip(),
                nome=(linha.get("nome") or "").strip(),
                turma=(linha.get("turma") or "").strip(),
                origem=caminho.name,
            )
            for numero, linha in enumerate(leitor, start=2)
        ]


def carregar_notas(caminho: str | Path) -> list[NotaBruta]:
    caminho = Path(caminho)
    with caminho.open(encoding="utf-8", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)
        return [
            NotaBruta(
                linha=numero,
                matricula=(linha.get("matricula") or "").strip(),
                disciplina=(linha.get("disciplina") or "").strip(),
                avaliacao=(linha.get("avaliacao") or "").strip(),
                nota=(linha.get("nota") or "").strip(),
                origem=caminho.name,
            )
            for numero, linha in enumerate(leitor, start=2)
        ]


def carregar_configuracao(caminho: str | Path) -> Configuracao:
    with Path(caminho).open(encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
    return Configuracao(
        media_aprovacao=float(dados["media_aprovacao"]),
        media_recuperacao=float(dados["media_recuperacao"]),
        nota_maxima=float(dados["nota_maxima"]),
    )
