from __future__ import annotations

import argparse
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / 'data' / 'processed' / 'candidatos_uem.parquet'


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


def main() -> None:
    parser = argparse.ArgumentParser(description='Remove o sufixo "- Uem" dos nomes dos cursos na base processada.')
    parser.add_argument('--input', type=Path, default=SOURCE_PATH, help='Caminho do parquet de entrada.')
    parser.add_argument('--output', type=Path, default=None, help='Caminho opcional do parquet de saída.')
    args = parser.parse_args()

    entrada = args.input
    saida = args.output or entrada.with_name('candidatos_uem_normalizado.parquet')
    df = pd.read_parquet(entrada)
    df_normalizado = normalizar_cursos_uem(df)
    saida.parent.mkdir(parents=True, exist_ok=True)
    df_normalizado.to_parquet(saida, index=False)

    print(f'Arquivo processado: {entrada}')
    print(f'Arquivo salvo: {saida}')
    print(f'Linhas: {len(df_normalizado):,}')
    print(f'Primeiros exemplos: {df_normalizado["UEM_Opc1"].dropna().head().tolist()}')


if __name__ == '__main__':
    main()
