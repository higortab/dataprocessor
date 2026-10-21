# DataProcessor CLI

Projeto executável usado nas Aulas 12–18 de Fundamentos de Python.

## Executar (CLI — Aula 15)

```bash
python -m dataprocessor \
  --clientes data/clientes.csv \
  --transacoes data/transacoes.csv \
  --config data/config.json \
  --formato texto \
  --output output/
```

## Menu interativo (Aulas 16–18)

```bash
python -m dataprocessor.interfaces.menu
```

- Aula 16: loop de menu e despacho de opções
- Aula 17: estado de sessão, validação de entrada e tratamento de erros
- Aula 18: `processar_caminhos()` isolada e testável (sem `input()`)

## Testar

```bash
python -m unittest discover -s tests -v
```
