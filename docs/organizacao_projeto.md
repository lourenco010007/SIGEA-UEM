# Organização e publicação do projeto

## Estrutura recomendada

| Caminho | Conteúdo | Deve ser versionado? |
|---|---|---|
| `notebooks/` | Código de limpeza, análise exploratória e integração de resultados | Sim, sem outputs que exponham registos pessoais |
| `scripts/` | Tarefas reutilizáveis de normalização, exportação e geração de resumos | Sim |
| `docs/` | Instruções, decisões de organização e dicionário dos campos | Sim, sem valores pessoais reais |
| `requirements.txt` | Dependências Python do projeto | Sim |
| `.vscode/extensions.json` | Recomendações de extensões | Sim |
| `data/raw/` | Planilhas originais de candidatos e apuramento | Não; manter em armazenamento local/autorizado |
| `data/processed/` | Parquet e Excel derivados das bases de candidatos | Não; contêm ou podem conter dados pessoais |
| `outputs/` | CSVs, gráficos e relatórios gerados | Não; recriar com os notebooks ou scripts |
| `.venv/`, `__pycache__/` | Ambiente e cache locais | Não |

As regras em `.gitignore` impedem a inclusão acidental de novos ficheiros locais nas categorias não versionadas. O Git continua a acompanhar ficheiros que já estavam versionados, mesmo depois de uma regra de exclusão ser adicionada.

## Decisão sobre ficheiros existentes

- Manter os três notebooks ativos: `dadosTeste_limpo.ipynb`, `EDA_procura_demografia.ipynb` e `merge_resultados_e_analise_target.ipynb`.
- Manter os scripts reutilizáveis em `scripts/` e a documentação necessária para executar e interpretar o projeto.
- Não voltar a colocar `dadosTeste.ipynb` no fluxo: é uma versão antiga substituída por `dadosTeste_limpo.ipynb`.
- Guardar os Parquet e Excel derivados em `data/processed/`, não em `notebooks/`. As versões locais atuais não são cópias binárias idênticas dos antigos Parquet versionados, pelo que não devem ser tratadas como simples renames.
- Tratar os CSVs e gráficos em `outputs/` como resultados reproduzíveis, não como fontes de verdade.
- `output.png` na raiz é um ficheiro de saída avulso; não faz parte do fluxo documentado.

## Duplicados e sobreposição

Na verificação local por SHA-256 não foram encontrados ficheiros binariamente idênticos entre os ficheiros de `data/processed/`, `notebooks/` e `outputs/`, nem nomes repetidos entre `data/processed/` e `notebooks/`. Existem, contudo, exportações em formatos ou recortes diferentes (por exemplo, Excel completo e por ano) e relatórios com temas relacionados. São variantes ou produtos gerados, não duplicados exatos.

## Bloqueio antes de publicar

Antes desta revisão, a árvore versionada continha ficheiros de origem e bases processadas com dados pessoais descritos em `dicionario_dados.md`, além de outputs gerados. A publicação desta organização remove esses artefactos do estado atual do repositório, preservando as cópias locais, e limpa os outputs guardados nos notebooks. A regra `.gitignore` evita que sejam adicionados novamente por engano.

Antes de criar um commit de publicação:

1. Manter os dados pessoais em armazenamento local/autorizado e não os adicionar ao Git.
2. Rever o diff final e confirmar que apenas código e documentação autorizados serão enviados.
3. Verificar a política institucional de autorização e privacidade para qualquer ficheiro de dados que se pretenda partilhar.

Remover um ficheiro do estado atual do Git não o apaga de commits anteriores. Se algum dado pessoal já foi publicado sem autorização, é necessário tratar a exposição e o histórico com os responsáveis pelo repositório e pela proteção de dados.

## Reprodução dos outputs

Com as dependências instaladas e a base processada disponível localmente:

```powershell
python scripts\generate_eda_outputs.py
python scripts\generate_eda_outputs.py --ano 2026
python scripts\export_candidatos_excel.py --ano 2026
```

Os dados necessários não são incluídos neste repositório; os comandos dependem de `data/processed/candidatos_uem.parquet`.
