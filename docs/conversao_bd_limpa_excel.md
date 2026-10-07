# Conversão da base limpa para Excel

## Objetivo

A base analítica de candidatos da UEM já foi tratada e salva em formato Parquet em `data/processed/candidatos_uem.parquet`. Para facilitar a exploração fora do VS Code, foi criada uma exportação em Excel mantendo a mesma base limpa sem perder as colunas essenciais do estudo.

## Origem e destino

- Origem: `data/processed/candidatos_uem.parquet`
- Destino: `data/processed/candidatos_uem.xlsx`
- Script reutilizável: `scripts/export_candidatos_excel.py`

## Comando de geração

Além da exportação para Excel, a base processada também pode ser normalizada para remover o sufixo `- Uem` nos nomes dos cursos com o script:

```powershell
python scripts\normalizar_cursos_uem.py
```

A exportação em Excel continua sendo feita com:

```powershell
python scripts\export_candidatos_excel.py
```

Para gerar uma versão filtrada por ano específico:

```powershell
python scripts\export_candidatos_excel.py --ano 2026
```

Isso cria automaticamente um arquivo como `data/processed/candidatos_uem_2026.xlsx`.

## Observações

- A conversão preserva todas as colunas da base processada.
- Os nomes dos cursos são normalizados para remover o sufixo `- Uem`, de modo que a análise e os relatórios não repitam a instituição no nome do curso.
- O arquivo Excel é adequado para exploração manual em ambiente autorizado; contém dados pessoais e só deve ser partilhado após validação formal.
- O nome e a estrutura dos campos mantêm a compatibilidade com os fluxos de análise em Python.
- O mesmo padrão pode ser reaproveitado para qualquer ano futuro, desde que a informação `Ano` esteja presente no dataset processado.

## Próximos passos recomendados

Conforme as anotações do documento de revisão, os próximos estudos devem priorizar:

- comparação de residência versus local de realização de exames;
- uso de faixas etárias em vez de idades isoladas;
- segmentação por país/província e por curso;
- análise de candidatos estrangeiros, com foco em país de origem e local de exame;
- geração de outputs por ano específico, mantendo a mesma estrutura de dados;
- consolidação da base de candidatos com os resultados do apuramento em um único conjunto analítico;
- retorno do foco principal para as províncias de residência e de realização dos exames, como dimensões centrais da análise.

A geração por ano foi implementada em `scripts/generate_eda_outputs.py`, que produz os resumos em `outputs/eda_procura_demografia/ano_2026/` quando o filtro `--ano 2026` é aplicado.

## Proteção de dados

A base contém dados pessoais e sensíveis do processo de admissão. O arquivo Excel deve ser tratado conforme as regras internas de privacidade e autorização de uso, e não deve ser publicado sem validação prévia.
