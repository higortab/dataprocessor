from .entidades import Aluno, AlunoBruto, Nota, NotaBruta
from .resultados import ErroRegistro


def validar_alunos(registros: list[AlunoBruto]) -> tuple[list[Aluno], list[ErroRegistro]]:
    validos: list[Aluno] = []
    erros: list[ErroRegistro] = []
    matriculas: set[str] = set()

    for registro in registros:
        if not registro.matricula or not registro.nome or not registro.turma:
            erros.append(ErroRegistro(registro.origem, registro.linha, "campo obrigatório vazio"))
            continue
        if not registro.matricula.isdigit():
            erros.append(
                ErroRegistro(
                    registro.origem,
                    registro.linha,
                    f"matrícula inválida ('{registro.matricula}')",
                )
            )
            continue
        if registro.matricula in matriculas:
            erros.append(
                ErroRegistro(
                    registro.origem,
                    registro.linha,
                    f"matrícula {registro.matricula} já cadastrada",
                )
            )
            continue
        matriculas.add(registro.matricula)
        validos.append(Aluno(registro.matricula, registro.nome, registro.turma))

    return validos, erros


def validar_notas(
    registros: list[NotaBruta],
    matriculas_validas: set[str],
    nota_maxima: float,
) -> tuple[list[Nota], list[ErroRegistro]]:
    validas: list[Nota] = []
    erros: list[ErroRegistro] = []
    avaliacoes: set[tuple[str, str, str]] = set()

    for registro in registros:
        if not registro.matricula or not registro.disciplina or not registro.avaliacao or registro.nota == "":
            erros.append(ErroRegistro(registro.origem, registro.linha, "campo obrigatório vazio"))
            continue
        try:
            valor = float(registro.nota)
        except ValueError:
            erros.append(
                ErroRegistro(
                    registro.origem,
                    registro.linha,
                    f"nota inválida ('{registro.nota}')",
                )
            )
            continue
        if valor < 0 or valor > nota_maxima:
            erros.append(
                ErroRegistro(
                    registro.origem,
                    registro.linha,
                    f"nota fora do intervalo ({valor})",
                )
            )
            continue
        if registro.matricula not in matriculas_validas:
            erros.append(
                ErroRegistro(
                    registro.origem,
                    registro.linha,
                    f"matrícula inexistente ({registro.matricula})",
                )
            )
            continue
        chave = (registro.matricula, registro.disciplina, registro.avaliacao)
        if chave in avaliacoes:
            erros.append(
                ErroRegistro(
                    registro.origem,
                    registro.linha,
                    f"avaliação já lançada ({registro.disciplina}/{registro.avaliacao})",
                )
            )
            continue
        avaliacoes.add(chave)
        validas.append(
            Nota(registro.matricula, registro.disciplina, registro.avaliacao, valor)
        )

    return validas, erros
