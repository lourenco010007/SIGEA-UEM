# Dicionário de Dados

## 1. Identificação do conjunto de dados

| Item | Informação |
|---|---|
| Projeto | Análise dos candidatos aos exames de admissão da UEM |
| Fonte principal | `data/raw/Dados Bibliograficos UEM_UZ_ISPQ 2025_2026.xls` |
| Dataset de saída | `data/processed/candidatos_uem.parquet` |
| Notebook responsável | `notebooks/dadosTeste_limpo.ipynb` |
| Unidade de análise | Um registro por candidato |
| Versão de referência | Branch `feature/tratamento-valores-nulos` |
| Referência temporal | Processo de admissão 2025/2026 |

## 2. Objetivo

Este documento descreve os dados utilizados no tratamento inicial dos candidatos, incluindo os campos mantidos, as transformações aplicadas e os campos removidos antes da gravação do arquivo Parquet.

## 3. Campos mantidos

A tabela abaixo documenta os campos identificados no fluxo atual do notebook. A confirmação definitiva do significado de cada campo deve ser feita junto ao dicionário oficial da planilha de origem.

| Campo | Tipo esperado | Descrição funcional | Tratamento no notebook |
|---|---|---|---|
| `Ano` | Inteiro | Ano do processo de admissão. | Mantido da fonte original. |
| `candidato_codigo` | Inteiro | Código único atribuído ao candidato no processo. | Mantido da fonte de tratamento; identifica o candidato e não representa o código do curso. |
| `apelido` | Texto | Apelido ou sobrenome do candidato. | Mantido da fonte original. |
| `nome` | Texto | Nome próprio ou nome completo do candidato. | Mantido da fonte original. |
| `Sexo` | Texto/categórico | Sexo informado pelo candidato. | Remoção de espaços nas extremidades e conversão para formato de título. |
| `EstCivil` | Texto/categórico | Estado civil do candidato. | Remoção de espaços nas extremidades e conversão para formato de título. |
| `DocIdent` | Texto | Número ou referência do documento de identificação. | Mantido da fonte; tratar como dado pessoal restrito. |
| `data_Nasc` | Data | Data de nascimento do candidato. | Mantida da fonte original. |
| `idade` | Inteiro nullable | Idade calculada para o ano de referência 2026. | Calculada como `2026 - ano(data_Nasc)`. |
| `TipoDoc` | Texto/categórico | Tipo de documento de identificação. | Mantido da fonte original. |
| `pais_nascimento` | Texto | País de nascimento do candidato. | Renomeado de `pai_nascimento`; texto normalizado. |
| `ProvNasc` | Texto/categórico | Província ou categoria de nascimento. | Registros com valor `Luanda` são recodificados como `Estrangeiro`; texto normalizado. |
| `ProvRes` | Texto/categórico | Província de residência do candidato. | Mantida da fonte de tratamento. |
| `ProvCand` | Texto/categórico | Província associada à candidatura. | Mantida da fonte original. |
| `cod_preUni` | Numérico ou texto | Código da instituição pré-universitária. | Mantido para análise de proveniência; a branch registra 29 valores ausentes. |
| `EscoPU` | Texto | Escola ou instituição pré-universitária de proveniência. | Remoção de espaços nas extremidades e conversão para formato de título. |
| `local_exame` | Texto | Local de realização do exame. | Texto normalizado. |
| `AnocPU` | Inteiro | Ano de conclusão do ensino pré-universitário. | Mantido da fonte de tratamento. |
| `distrito_nascimento` | Texto | Distrito de nascimento do candidato. | Registros recodificados como estrangeiros recebem `Estrangeiro`; texto normalizado. |
| `distrito_residencia` | Texto | Distrito de residência do candidato. | Remoção de espaços nas extremidades e conversão para formato de título. |
| `UEM_Cod_Opc1` | Numérico inteiro | Código da primeira opção de curso na UEM. | Convertido para inteiro. |
| `UEM_Opc1` | Texto | Descrição da primeira opção de curso na UEM. | Remoção de espaços nas extremidades e conversão para formato de título. |
| `UEM_Cod_Opc2` | Numérico inteiro | Código da segunda opção de curso na UEM. | Valores ausentes preenchidos com `0` e convertidos para inteiro. |
| `UEM_Opc2` | Texto | Descrição da segunda opção de curso na UEM. | Valores ausentes preenchidos com `Sem Opcao`; texto normalizado. |

> A branch de tratamento apresenta 24 campos no resultado analisado. Os campos de código devem ser interpretados conforme a finalidade: `candidato_codigo` identifica o candidato, `cod_preUni` identifica a instituição pré-universitária e `UEM_Cod_Opc1`/`UEM_Cod_Opc2` identificam as opções de curso. Eles não devem ser misturados em análises de frequência ou chaves de curso.

## 4. Campos removidos

### 4.1 Campos operacionais e pessoais

| Campo | Motivo da remoção |
|---|---|
| `Direct` | Campo operacional não utilizado na análise. |
| `Ordem` | Ordem operacional do registro. |
| `NoLido` | Indicador técnico de leitura. |
| `Dispensa` | Informação operacional fora do escopo atual. |
| `RevProva` | Informação operacional de revisão de prova. |
| `celular` | Dado de contacto pessoal não utilizado nesta etapa. |
| `celularAlternativo` | Dado de contacto pessoal não utilizado nesta etapa. |
| `DataReg` | Data operacional de registro. |
| `HoraReg` | Hora operacional de registro. |
| `OperReg` | Identificação do operador do registro. |

### 4.2 Opções de outras instituições

| Campo | Motivo da remoção |
|---|---|
| `ISPQ_Opc1` | Opção de curso de outra instituição, fora do recorte atual. |
| `ISPQ_Cod_Opc2` | Código de opção de outra instituição. |
| `UZ_Cod_Opc1` | Código de opção de outra instituição. |
| `UZ_Opc1` | Opção de curso de outra instituição. |
| `ISPQ_Opc2` | Segunda opção de outra instituição. |
| `UZ_Opc2` | Segunda opção de outra instituição. |
| `ISPQ_Cod_Opc1` | Código de opção de outra instituição. |
| `UZ_Cod_Opc2` | Código de opção de outra instituição. |

### 4.3 Outros campos excluídos

| Campo | Motivo da remoção |
|---|---|
| `Status` | Estado operacional não utilizado na análise atual. |
| `nuit` | Identificador pessoal sensível não utilizado na análise atual. |
| `TipoEst` | Tipo de estudante excluído do recorte atual. |
| `Classif` | Classificação excluída do recorte atual. |

## 5. Regras de transformação

1. `pai_nascimento` é renomeado para `pais_nascimento`.
2. É aplicada uma tentativa de correção de codificação de texto, tratando casos de mojibake.
3. São mantidos os registros que possuem pelo menos uma informação nas colunas de opção da UEM:
   - `UEM_Cod_Opc1`
   - `UEM_Opc1`
   - `UEM_Cod_Opc2`
   - `UEM_Opc2`
4. `UEM_Cod_Opc2` recebe `0` quando está ausente.
5. `UEM_Opc2` recebe `Sem Opcao` quando está ausente.
6. Os campos textuais selecionados são normalizados com `strip().title()`.
7. Os campos `TipoEst` e `Classif` são removidos.
8. O resultado é exportado para `data/processed/candidatos_uem.parquet`.

## 6. Dicionário específico dos campos de código

| Campo | Papel | Pode ser nulo? | Regra de interpretação |
|---|---|---:|---|
| `candidato_codigo` | Identificador do candidato | Não observado na saída da branch | Chave do candidato no processo; não é código de curso. |
| `cod_preUni` | Identificador da instituição pré-universitária | Sim; 29 nulos observados na branch | Ausência significa que a instituição não possui código informado ou não foi associada. |
| `UEM_Cod_Opc1` | Código da primeira opção UEM | Não observado entre os registros filtrados | Relacionar com o cadastro oficial de cursos da UEM. |
| `UEM_Cod_Opc2` | Código da segunda opção UEM | Pode ser ausente na origem | Ausência é convertida para `0`, que representa `Sem Opcao`. |

O campo de código incorporado pela branch de tratamento, `candidato_codigo`, deve aparecer separadamente de `cod_preUni`. O primeiro identifica a pessoa/candidatura; o segundo identifica a instituição de proveniência.

 


