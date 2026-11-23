from collections import defaultdict

from ..core.entidades import Aluno, AlunoBruto, Configuracao, NotaBruta
from ..core.metricas import medias_por_disciplina
from ..core.resultados import ResultadoProcessamento
from ..core.validador import validar_alunos, validar_notas


def executar_processamento(
    alunos_brutos: list[AlunoBruto],
    notas_brutas: list[NotaBruta],
    configuracao: Configuracao,
) -> ResultadoProcessamento:
    alunos, erros_alunos = validar_alunos(alunos_brutos)
    matriculas = {aluno.matricula for aluno in alunos}
    notas, erros_notas = validar_notas(notas_brutas, matriculas, configuracao.nota_maxima)

    notas_por_aluno: dict[str, list[float]] = defaultdict(list)
    for nota in notas:
        notas_por_aluno[nota.matricula].append(nota.valor)

    alunos_com_notas = tuple(
        Aluno(aluno.matricula, aluno.nome, aluno.turma, tuple(notas_por_aluno[aluno.matricula]))
        for aluno in alunos
    )
    notas_validas = tuple(notas)
    return ResultadoProcessamento(
        alunos=alunos_com_notas,
        notas=notas_validas,
        erros=tuple(erros_alunos + erros_notas),
        configuracao=configuracao,
        medias_disciplina=medias_por_disciplina(notas_validas),
        notas_invalidas=len(erros_notas),
    )
