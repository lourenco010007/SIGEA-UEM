# Analise de procura e demografia UEM 2026

Projeto de analise exploratoria dos candidatos e da procura por cursos da UEM para 2026. O trabalho e desenvolvido em notebooks Jupyter, usando planilhas Excel como entrada e arquivos CSV como resultados consolidados.

## Requisitos

- Windows, macOS ou Linux.
- Python 3.11 ou superior. O ambiente local atual usa Python 3.14.3.
- VS Code com as extensoes recomendadas em `.vscode/extensions.json`.
- Arquivos de dados locais em `data/raw/`. Essa pasta esta no `.gitignore` porque pode conter dados pessoais ou arquivos grandes.

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

- `Dados Bibliograficos UEM_UZ_ISPQ 2025_2026.xls`: dados bibliograficos dos candidatos. O formato `.xls` requer o pacote `xlrd`.
- `Cursos_UEM_2026.xlsx`: cadastro e procura dos cursos.
- `UEMResultadosFinal-APURAMENTO2026.xlsx`: resultados finais do apuramento.
- `CTA-Apuramento2026.xlsx`: dados do CTA.
- `PARENTES-Apuramento2026.xlsx`: dados de parentes.

Existe tambem um arquivo processado em `data/processed/candidatos_uem.parquet`.

## Ordem dos notebooks

1. `notebooks/dadosTeste.ipynb`: exploracao inicial. E um rascunho historico e ainda usa um caminho relativo antigo; nao e o ponto de entrada recomendado.
2. `notebooks/dadosTeste_limpo.ipynb`: leitura e limpeza inicial dos dados bibliograficos.
3. `notebooks/EDA_procura_demografia.ipynb`: analise exploratoria da procura e do perfil demografico. Gera os CSVs em `outputs/eda_procura_demografia/`.
4. `notebooks/merge_resultados_e_analise_target.ipynb`: combinacao dos resultados do apuramento e analise do alvo. Deve ser executado depois que as entradas correspondentes estiverem disponiveis.

Antes de executar um notebook, confirme que o diretorio de trabalho e a pasta `notebooks/`, pois os caminhos relativos foram escritos a partir dela. No VS Code, a opcao **Run All** normalmente respeita a pasta do arquivo; se houver erro de caminho, abra a raiz do projeto como workspace e ajuste o diretorio de trabalho do kernel.

## Saidas geradas

`notebooks/EDA_procura_demografia.ipynb` produz resumos por curso, provincia, distrito, pais, escola, ano de conclusao, genero, idade e migracao. Os arquivos ficam em `outputs/eda_procura_demografia/`.

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

- O notebook `dadosTeste.ipynb` registra uma tentativa antiga de ler o arquivo sem `data/raw/` e uma chamada `drop` com lista aninhada; use `dadosTeste_limpo.ipynb` para o fluxo corrigido.
- Os notebooks contem celulas de instalacao, como `%pip install matplotlib`. A instalacao deve ser feita pelo `requirements.txt` para manter o ambiente consistente.
- Os nomes e caminhos dos arquivos de dados precisam permanecer exatamente iguais aos referenciados nos notebooks, ou os caminhos devem ser atualizados antes da execucao.
- Os dados brutos nao devem ser publicados sem verificar as regras de privacidade e autorizacao aplicaveis.