# main.py
from leitor import carregar_clientes, carregar_transacoes, carregar_config
from validador import validar_cliente, validar_transacao, separar_registros
from transformador import transformar_clientes, transformar_transacoes
from processador import total_aprovado, media_idade

clientes_raw = carregar_clientes("data/clientes.csv")
transacoes_raw = carregar_transacoes("data/transacoes.csv")
config = carregar_config("data/config.json")

clientes_validos, clientes_invalidos = separar_registros(
    clientes_raw, validar_cliente
)
ids_validos = {c["id"] for c in clientes_validos}

transacoes_validas, transacoes_invalidas = separar_registros(
    transacoes_raw, validar_transacao,
    ids_clientes=ids_validos, config=config
)

clientes = transformar_clientes(clientes_validos)
transacoes = transformar_transacoes(transacoes_validas)

print("=== RELATÓRIO FINAL — DataProcessor ===")
print(f"CLIENTES PROCESSADOS ({len(clientes)} válidos de {len(clientes_raw)}):")
for c in clientes:
    print(f"  ID {c['id']} | {c['nome']} | {c['email']} | {c['idade']} | {c['cidade']}")
print(f"CLIENTES REJEITADOS ({len(clientes_invalidos)} inválidos de {len(clientes_raw)}):")
for item in clientes_invalidos:
    c = item["registro"]
    erros = item["erros"]
    print(f"  ID {c.get('id', 'N/A')} - {c.get('nome', 'N/A')}: {', '.join(erros)}")

print(f"TRANSACOES PROCESSADAS ({len(transacoes)} válidas de {len(transacoes_raw)}):")
for t in transacoes_validas:
    print(f"  ID {t['id']} | Cliente {t['cliente_id']} | R$ {t['valor']:.2f} | {t['categoria']} | Status: {t['status']}")
print(f"TRANSACOES REJEITADAS ({len(transacoes_invalidas)} inválidas de {len(transacoes_raw)}):")
for item in transacoes_invalidas:
    t = item["registro"]
    erros = item["erros"]
    print(f"  ID {t.get('id', 'N/A')} - Cliente {t.get('cliente_id', 'N/A')}: {', '.join(erros)}")

print("MÉTRICAS")
print(f"Total aprovado: R$ {total_aprovado(transacoes):.2f}")
print(f"Média de idade: {media_idade(clientes):.2f}")