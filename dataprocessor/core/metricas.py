def media_idade(clientes):
    idades_validas = [c.idade for c in clientes if c.idade and c.idade > 0]
    if not idades_validas:
        return 0
    return sum(idades_validas) / len(idades_validas)


def extremos_idade(clientes):
    idades_validas = [c.idade for c in clientes if c.idade and c.idade > 0]
    if not idades_validas:
        return None, None
    return min(idades_validas), max(idades_validas)


def contar_por_cidade(clientes):
    contagem = {}
    for cliente in clientes:
        cidade = cliente.cidade
        contagem[cidade] = contagem.get(cidade, 0) + 1
    return contagem


def transacoes_aprovadas(transacoes):
    return [t for t in transacoes if t.esta_aprovada and t.valor and t.valor > 0]


def total_aprovado(transacoes):
    return sum(t.valor for t in transacoes_aprovadas(transacoes))


def ticket_medio_aprovado(transacoes):
    aprovadas = transacoes_aprovadas(transacoes)
    if not aprovadas:
        return 0
    return sum(t.valor for t in aprovadas) / len(aprovadas)
