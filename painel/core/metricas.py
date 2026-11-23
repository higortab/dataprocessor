from collections import defaultdict
from collections.abc import Iterable

from .entidades import Nota


def medias_por_disciplina(notas: Iterable[Nota]) -> dict[str, float]:
    grupos: dict[str, list[float]] = defaultdict(list)
    for nota in notas:
        grupos[nota.disciplina].append(nota.valor)
    return {disciplina: sum(valores) / len(valores) for disciplina, valores in grupos.items()}
