from __future__ import annotations

import argparse
import re
from pathlib import Path

import pandas as pd
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / 'data' / 'processed' / 'candidatos_uem.parquet'
DEFAULT_OUTPUT_DIR = ROOT / 'outputs' / 'eda_procura_demografia'

PROVINCIAS = {
    'cabo delgado': 'Cabo Delgado',
    'gaza': 'Gaza',
    'inhambane': 'Inhambane',
    'manica': 'Manica',
    'maputo': 'Maputo',
    'nampula': 'Nampula',
    'niassa': 'Niassa',
    'sofala': 'Sofala',
    'tete': 'Tete',
    'zambezia': 'Zambézia',
    'quissico': 'Inhambane',
    'cidade de maputo': 'Maputo',
    'provincia de maputo': 'Maputo',
    'cidade da beira': 'Sofala',
    'beira': 'Sofala',
    'chimoio': 'Manica',
    'xai xai': 'Gaza',
    'nacala': 'Nampula',
    'quelimane': 'Zambézia',
}


def normalizar_texto(valor):
    if pd.isna(valor):
        return ''
    texto = unicodedata.normalize('NFKD', str(valor))
    texto = ''.join(caractere for caractere in texto if not unicodedata.combining(caractere))
    texto = ' '.join(texto.casefold().split())
    return texto


def normalizar_provincia(valor):
    texto = normalizar_texto(valor)
    if not texto:
        return 'Desconhecida'
    for chave, nome in PROVINCIAS.items():
        if chave in texto:
            return nome
    return texto.title()


def normalizar_curso(valor):
    if pd.isna(valor):
        return 'Sem Opcao'
    texto = str(valor).replace('–', '-').replace('—', '-')
    texto = re.sub(r'\s*-\s*(?:UEM|Uem|uem)\s*$', '', texto, flags=re.IGNORECASE)
    texto = re.sub(r'\s*-\s*$', '', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto or 'Sem Opcao'


def normalizar_cursos_uem(df: pd.DataFrame) -> pd.DataFrame:
    df_limpo = df.copy()
    for coluna in ['UEM_Opc1', 'UEM_Opc2']:
        if coluna in df_limpo.columns:
            df_limpo[coluna] = df_limpo[coluna].fillna('Sem Opcao').map(normalizar_curso)
    return df_limpo


def definir_ano_saida(ano: int | None) -> str:
    return f'ano_{ano}' if ano is not None else 'geral'


def gerar_output_dir(ano: int | None) -> Path:
    base_dir = DEFAULT_OUTPUT_DIR / definir_ano_saida(ano)
    base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir


def salvar_csv(df: pd.DataFrame, nome_arquivo: str, output_dir: Path) -> Path:
    caminho = output_dir / nome_arquivo
    df.to_csv(caminho, index=False)
    return caminho


def qualificar_ano(df: pd.DataFrame, ano: int | None) -> pd.DataFrame:
    if ano is None:
        return df.copy()
    return df[df['Ano'] == int(ano)].copy()


def montar_resumo_contagem(df: pd.DataFrame, coluna: str, nome_coluna_saida: str) -> pd.DataFrame:
    resumo = df[coluna].fillna('Desconhecida').astype(str).value_counts().reset_index()
    resumo.columns = [nome_coluna_saida, 'total']
    return resumo.sort_values('total', ascending=False).reset_index(drop=True)


def montar_resumo_provincia_residencia(df: pd.DataFrame) -> pd.DataFrame:
    df_local = df[['ProvRes']].copy()
    df_local['ProvRes'] = df_local['ProvRes'].map(normalizar_provincia)
    return montar_resumo_contagem(df_local, 'ProvRes', 'provincia_residencia')


def montar_resumo_provincia_exame(df: pd.DataFrame) -> pd.DataFrame:
    df_local = df[['local_exame']].copy()
    df_local['local_exame'] = df_local['local_exame'].map(normalizar_provincia)
    return montar_resumo_contagem(df_local, 'local_exame', 'provincia_realizacao_exame')


def montar_cruzamento_residencia_exame(df: pd.DataFrame) -> pd.DataFrame:
    tabela = df[['ProvRes', 'local_exame']].copy()
    tabela['provincia_residencia'] = tabela['ProvRes'].map(normalizar_provincia)
    tabela['provincia_realizacao_exame'] = tabela['local_exame'].map(normalizar_provincia)
    cruzamento = pd.crosstab(
        tabela['provincia_residencia'],
        tabela['provincia_realizacao_exame'],
    ).reset_index()
    cruzamento.columns = ['provincia_residencia', *[str(col) for col in cruzamento.columns[1:]]]
    return cruzamento


def gerar_analise(df: pd.DataFrame, output_dir: Path) -> list[Path]:
    arquivos = []

    arquivos.append(
        salvar_csv(montar_resumo_contagem(df, 'UEM_Opc1', 'curso'), 'resumo_procura_por_curso.csv', output_dir)
    )
    arquivos.append(
        salvar_csv(montar_resumo_contagem(df, 'Sexo', 'sexo'), 'resumo_genero_por_curso.csv', output_dir)
    )
    arquivos.append(
        salvar_csv(montar_resumo_contagem(df, 'ProvRes', 'provincia'), 'resumo_por_provincia.csv', output_dir)
    )
    arquivos.append(
        salvar_csv(montar_resumo_provincia_residencia(df), 'resumo_por_provincia_residencia.csv', output_dir)
    )
    arquivos.append(
        salvar_csv(montar_resumo_provincia_exame(df), 'resumo_por_provincia_local_exame.csv', output_dir)
    )
    arquivos.append(
        salvar_csv(montar_cruzamento_residencia_exame(df), 'resumo_migracao_provincia_residencia_exame.csv', output_dir)
    )
    arquivos.append(
        salvar_csv(montar_resumo_contagem(df, 'distrito_residencia', 'distrito'), 'resumo_por_distrito.csv', output_dir)
    )
    arquivos.append(
        salvar_csv(montar_resumo_contagem(df, 'pais_nascimento', 'pais'), 'resumo_por_pais.csv', output_dir)
    )
    arquivos.append(
        salvar_csv(montar_resumo_contagem(df, 'EscoPU', 'escola'), 'resumo_por_escola.csv', output_dir)
    )
    arquivos.append(
        salvar_csv(montar_resumo_contagem(df, 'AnocPU', 'ano_conclusao'), 'resumo_por_ano_conclusao.csv', output_dir)
    )
    arquivos.append(
        salvar_csv(montar_resumo_contagem(df, 'Sexo', 'sexo').rename(columns={'sexo': 'sexo', 'total': 'total_candidatos'}), 'resumo_sexo.csv', output_dir)
    )

    faixa = df['data_Nasc'].dropna()
    if not faixa.empty:
        idade = pd.to_datetime(faixa, errors='coerce').dt.year
        # like 2026 census year; keep a stable value and save the distribution
        idade_ano = 2026 - idade
        idade_df = idade_ano.dropna().astype(int).value_counts().reset_index()
        idade_df.columns = ['idade', 'total']
        arquivos.append(salvar_csv(idade_df.sort_values('idade').reset_index(drop=True), 'resumo_idade_por_curso.csv', output_dir))

    return arquivos


def main() -> None:
    parser = argparse.ArgumentParser(description='Gera os resumos exploratórios da procura e demografia por ano específico.')
    parser.add_argument('--ano', type=int, default=None, help='Filtra por um ano específico, ex.: --ano 2026')
    parser.add_argument('--output-dir', type=Path, default=DEFAULT_OUTPUT_DIR, help='Diretório para os arquivos CSV gerados')
    args = parser.parse_args()

    df = pd.read_parquet(SOURCE_PATH)
    df = normalizar_cursos_uem(df)
    df_filtrado = qualificar_ano(df, args.ano)
    output_dir = Path(args.output_dir)
    if args.ano is not None:
        output_dir = output_dir / definir_ano_saida(args.ano)
    output_dir.mkdir(parents=True, exist_ok=True)

    arquivos = gerar_analise(df_filtrado, output_dir)
    print(f'Arquivo base: {SOURCE_PATH}')
    print(f'Ano filter: {args.ano if args.ano is not None else "todos"}')
    print(f'Linhas processadas: {len(df_filtrado):,}')
    print(f'Pasta destino: {output_dir}')
    print(f'Arquivos gerados: {len(arquivos)}')

    for caminho in arquivos:
        print(f'- {caminho.name}')


if __name__ == '__main__':
    main()
