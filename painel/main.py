import argparse
import logging
from pathlib import Path

from .infra.arquivos import carregar_alunos, carregar_configuracao, carregar_notas
from .infra.relatorios import criar_gerador
from .services.processamento import executar_processamento


def configurar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Consolida as notas da turma e informa a situação de cada aluno.")
    parser.add_argument("--alunos", required=True, help="Caminho do CSV de alunos.")
    parser.add_argument("--notas", required=True, help="Caminho do CSV de notas.")
    parser.add_argument("--config", required=True, help="Caminho do JSON de configuração.")
    parser.add_argument("--formato", choices=("texto", "json"), default="texto")
    parser.add_argument("--output", type=Path, default=Path("output"))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = configurar_parser().parse_args(argv)
    try:
        args.output.mkdir(parents=True, exist_ok=True)
        log_path = args.output / "painel.log"
        logging.basicConfig(
            filename=log_path,
            level=logging.INFO,
            format="%(asctime)s %(levelname)s %(message)s",
            force=True,
        )
        logging.info("Iniciando processamento")
        resultado = executar_processamento(
            carregar_alunos(args.alunos),
            carregar_notas(args.notas),
            carregar_configuracao(args.config),
        )
        relatorio = criar_gerador(args.formato).render(resultado)
        nome = "relatorio.txt" if args.formato == "texto" else "relatorio.json"
        (args.output / nome).write_text(relatorio, encoding="utf-8")
        logging.info(
            "Processamento concluído: %d alunos e %d notas válidas",
            len(resultado.alunos),
            len(resultado.notas),
        )
        print(relatorio, end="")
        return 0
    except (OSError, ValueError, KeyError, TypeError) as erro:
        logging.exception("Falha no processamento")
        print(f"[ERRO] {erro}")
        return 1
