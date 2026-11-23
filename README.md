# Painel de Notas da Turma

Projeto final de Fundamentos de Python. Lê alunos e notas em CSV, valida os registros sem interromper o processamento, calcula médias e situação e gera relatório em texto ou JSON.

A regra de negócio fica em `painel/core`, a leitura e a escrita de arquivos ficam em `painel/infra`, e a linha de comando só recebe os argumentos e chama o service.

## Executar

```bash
python -m painel \
  --alunos data/alunos.csv \
  --notas data/notas.csv \
  --config data/config.json \
  --formato json \
  --output output/
```

`--formato` aceita `texto` ou `json`. A pasta `output/` é criada se não existir. O relatório sai em `output/relatorio.txt` ou `output/relatorio.json`, e o log em `output/painel.log`.

## Testar

```bash
python -m unittest discover -s tests -v
```

Os testes usam dados em memória ou arquivos temporários. Não dependem dos CSVs de `data/`.
