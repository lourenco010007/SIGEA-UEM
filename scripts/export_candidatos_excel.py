from __future__ import annotations

import argparse
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / 'data' / 'processed' / 'candidatos_uem.parquet'
OUTPUT_DIR = ROOT / 'data' / 'processed'


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


def exportar_candidatos(ano: int | None = None, output_path: Path | None = None) -> Path:
    df = pd.read_parquet(SOURCE_PATH)
    df = normalizar_cursos_uem(df)

    if ano is not None:
        df = df[df['Ano'] == int(ano)].copy()
        nome_arquivo = f'candidatos_uem_{ano}.xlsx'
    else:
        nome_arquivo = 'candidatos_uem.xlsx'

    destino = output_path or (OUTPUT_DIR / nome_arquivo)
    destino.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(destino, index=False, engine='openpyxl')
    return destino


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Exporta a base limpa de candidatos da UEM para Excel.'
    )
    parser.add_argument(
        '--ano',
        type=int,
        default=None,
        help='Opcional: filtra a exportacao para um ano especifico, por exemplo --ano 2026.',
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=None,
        help='Caminho opcional do arquivo Excel de saída.',
    )
    args = parser.parse_args()

    destino = exportar_candidatos(ano=args.ano, output_path=args.output)
    print(f'Arquivo gerado: {destino}')


if __name__ == '__main__':
    main()
