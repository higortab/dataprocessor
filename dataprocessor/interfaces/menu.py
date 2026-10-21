from pathlib import Path

from ..infra.fontes import fonte_a_partir_de_caminhos
from ..infra.relatorios import criar_gerador
from ..services.processamento import executar_processamento

FORMATOS_VALIDOS = {"texto", "json", "csv"}
OPCOES_VALIDAS = {"1", "2", "3", "4"}


def processar_caminhos(caminho_clientes, caminho_transacoes, caminho_config):
    fonte = fonte_a_partir_de_caminhos(caminho_clientes, caminho_transacoes, caminho_config)
    return executar_processamento(fonte)


def _pedir_formato():
    formato = input("Formato (texto/json/csv) [texto]: ").strip() or "texto"
    if formato not in FORMATOS_VALIDOS:
        print(f"Formato inválido: '{formato}'.")
        return None
    return formato


def processar():
    caminho_clientes = (
        input("Caminho do CSV de clientes [data/clientes.csv]: ").strip()
        or "data/clientes.csv"
    )
    caminho_transacoes = (
        input("Caminho do CSV de transações [data/transacoes.csv]: ").strip()
        or "data/transacoes.csv"
    )
    caminho_config = (
        input("Caminho do JSON de config [data/config.json]: ").strip()
        or "data/config.json"
    )

    try:
        resultado = processar_caminhos(caminho_clientes, caminho_transacoes, caminho_config)
    except (OSError, ValueError, KeyError) as erro:
        print(f"[ERRO] Não foi possível processar: {erro}")
        return None

    print(f"Clientes válidos: {len(resultado.clientes)}")
    print(f"Transações válidas: {len(resultado.transacoes)}")
    return resultado


def exibir_relatorio(resultado):
    formato = _pedir_formato()
    if formato is None:
        return
    print(criar_gerador(formato).render(resultado))


def salvar_relatorio(resultado):
    formato = _pedir_formato()
    if formato is None:
        return
    pasta = Path(input("Pasta de saída [output]: ").strip() or "output")
    pasta.mkdir(parents=True, exist_ok=True)
    nome = "relatorio.txt" if formato == "texto" else f"relatorio.{formato}"
    caminho = pasta / nome
    caminho.write_text(criar_gerador(formato).render(resultado), encoding="utf-8")
    print(f"Relatório salvo em {caminho}")


def menu_principal():
    resultado = None
    while True:
        print("\n=== DataProcessor — Menu ===")
        print("1. Processar dados")
        print("2. Exibir relatório")
        print("3. Salvar relatório em arquivo")
        print("4. Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao not in OPCOES_VALIDAS:
            print(f"Opção inválida: '{opcao}'. Escolha 1, 2, 3 ou 4.")
            continue

        if opcao == "1":
            novo_resultado = processar()
            if novo_resultado is not None:
                resultado = novo_resultado
        elif opcao == "2":
            if resultado is None:
                print("Nenhum dado processado ainda. Escolha a opção 1 primeiro.")
                continue
            exibir_relatorio(resultado)
        elif opcao == "3":
            if resultado is None:
                print("Nenhum dado processado ainda. Escolha a opção 1 primeiro.")
                continue
            salvar_relatorio(resultado)
        elif opcao == "4":
            break


if __name__ == "__main__":
    menu_principal()
