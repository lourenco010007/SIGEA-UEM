# SISTEMA INTELIGENTE DE GESTAO DE EXAMES DE ADMISSAO

Projeto de analise exploratoria dos candidatos e da procura por cursos da UEM para 2026. O trabalho e desenvolvido em notebooks Jupyter, usando planilhas Excel como entrada e arquivos CSV como resultados consolidados.

## Requisitos

- Windows, macOS ou Linux.
- Python 3.11 ou superior. O ambiente local atual usa Python 3.14.3.
- VS Code com as extensoes recomendadas em `.vscode/extensions.json`.
- Arquivos de entrada locais em `data/raw/`. Os ficheiros podem conter dados pessoais e não devem ser publicados.

## Organização do projeto

- `data/raw/`: ficheiros de origem, mantidos apenas no ambiente autorizado.
- `data/processed/`: bases Parquet e exportações Excel geradas localmente.
- `notebooks/`: notebooks de limpeza, análise exploratória e integração dos resultados.
- `scripts/`: tarefas reutilizáveis de normalização e geração/exportação de resumos.
- `outputs/`: tabelas e gráficos gerados; podem ser recriados pelos notebooks e scripts.
- `docs/`: documentação do projeto e dos dados.

As regras de `.gitignore` evitam adicionar novos dados e outputs por engano. Elas **não deixam de controlar ficheiros já versionados**; consulte [docs/organizacao_projeto.md](docs/organizacao_projeto.md) antes de preparar uma publicação.

## Instalacao no Windows

No PowerShell, a partir da raiz do projeto:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Se a politica do PowerShell impedir a ativacao, use diretamente o executavel do ambiente:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

No VS Code, selecione o interpretador `.venv\Scripts\python.exe` e escolha o mesmo ambiente como kernel dos notebooks.

## Dados de entrada

Os notebooks atualmente referenciam estes arquivos em `data/raw/`:

- Os ficheiros de entrada não são distribuídos neste repositório; coloque cópias autorizadas nessa pasta localmente.
- `Dados Bibliograficos UEM_UZ_ISPQ 2025_2026.xls`: dados bibliograficos dos candidatos. O formato `.xls` requer o pacote `xlrd`.
- `Cursos_UEM_2026.xlsx`: cadastro e procura dos cursos.
- `UEMResultadosFinal-APURAMENTO2026.xlsx`: resultados finais do apuramento.
- `CTA-Apuramento2026.xlsx`: dados do CTA.
- `PARENTES-Apuramento2026.xlsx`: dados de parentes.

A base processada `data/processed/candidatos_uem.parquet` é um ficheiro local gerado pelo notebook de limpeza; não é distribuída neste repositório.

## Ordem dos notebooks

1. `notebooks/dadosTeste_limpo.ipynb`: leitura e limpeza inicial dos dados bibliograficos.
2. `notebooks/EDA_procura_demografia.ipynb`: analise exploratoria da procura e do perfil demografico. Gera os CSVs em `outputs/eda_procura_demografia/`.
3. `notebooks/merge_resultados_e_analise_target.ipynb`: combinacao dos resultados do apuramento e analise do alvo. Deve ser executado depois que as entradas correspondentes estiverem disponiveis.

Antes de executar um notebook, confirme que o diretorio de trabalho e a pasta `notebooks/`, pois os caminhos relativos foram escritos a partir dela. No VS Code, a opcao **Run All** normalmente respeita a pasta do arquivo; se houver erro de caminho, abra a raiz do projeto como workspace e ajuste o diretorio de trabalho do kernel.

## Saidas geradas

`notebooks/EDA_procura_demografia.ipynb` produz resumos por curso, provincia, distrito, pais, escola, ano de conclusao, genero, idade e migracao. Os arquivos ficam em `outputs/eda_procura_demografia/`.

Os nomes dos cursos na base processada são normalizados para remover o sufixo `- Uem`, mantendo apenas o nome do curso e a modalidade, por exemplo `Medicina - Diurno` em vez de `Medicina - Diurno - Uem`.

Para manter a estrutura compatível com a observação de que todos os outputs devem ser geráveis por ano específico, também existe um script reutilizável que gera os mesmos resumos por ano e reforça as dimensões relevantes de análise:

- `ProvRes` (província de residência)
- `local_exame` (local de realização de exames)
- cruzamento `provincia_residencia x provincia_realizacao_exame`

```powershell
python scripts\generate_eda_outputs.py
python scripts\generate_eda_outputs.py --ano 2026
```

Os outputs gerais ficam em `outputs/eda_procura_demografia/`; a versão anual é escrita em `outputs/eda_procura_demografia/ano_2026/`.

A base limpa pode ser normalizada sem sobrescrever o Parquet original; por omissão, o resultado fica em `data/processed/candidatos_uem_normalizado.parquet`. Também pode ser exportada para Excel para uso externo em exploração manual e validação:

```powershell
python scripts\normalizar_cursos_uem.py
python scripts\export_candidatos_excel.py
python scripts\export_candidatos_excel.py --ano 2026
```

O arquivo principal fica em `data/processed/candidatos_uem.xlsx`; a versão filtrada por ano é criada automaticamente quando solicitado.

## Extensoes do VS Code

Obrigatorias para o fluxo atual:

- **Python** (`ms-python.python`): interpretador, ambientes virtuais e execucao Python.
- **Jupyter** (`ms-toolsai.jupyter`): abertura e execucao de notebooks `.ipynb`.
- **Pylance** (`ms-python.vscode-pylance`): analise de codigo, autocomplete e diagnosticos Python.

Opcional: uma extensao de visualizacao de Excel pode facilitar a inspecao manual das planilhas, mas nao e necessaria para executar os notebooks.

## Verificacao rapida

Depois da instalacao, valide o ambiente com:

```powershell
.\.venv\Scripts\python.exe -c "import pandas, numpy, matplotlib, openpyxl, xlrd, IPython; print('Ambiente OK')"
```

Para executar notebooks pelo terminal:

```powershell
.\.venv\Scripts\python.exe -m jupyter notebook
```

## Observacoes conhecidas

- O notebook antigo `dadosTeste.ipynb` foi removido do fluxo; use `dadosTeste_limpo.ipynb` para o tratamento inicial.
- Os notebooks contem celulas de instalacao, como `%pip install matplotlib`. A instalacao deve ser feita pelo `requirements.txt` para manter o ambiente consistente.
- Os nomes e caminhos dos arquivos de dados precisam permanecer exatamente iguais aos referenciados nos notebooks, ou os caminhos devem ser atualizados antes da execucao.
- Os dados brutos nao devem ser publicados sem verificar as regras de privacidade e autorizacao aplicaveis.