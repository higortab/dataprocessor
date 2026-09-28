# DataProcessor CLI

Projeto executável usado nas Aulas 12–16 de Fundamentos de Python.

## Executar (CLI — Aula 15)

```bash
python -m dataprocessor \
  --clientes data/clientes.csv \
  --transacoes data/transacoes.csv \
  --config data/config.json \
  --formato texto \
  --output output/
```

## Menu interativo (Aula 16)

```bash
python -m dataprocessor.interfaces.menu
```

## Testar

```bash
python -m unittest discover -s tests -v
```
