"""Banco SQLite: pedidos, rotas calculadas e histórico. O esquema já está pronto. As consultas são TODO."""

import sqlite3
from pathlib import Path

import pandas as pd

CAMINHO_BANCO = Path(__file__).resolve().parent.parent / "rotacerta.db"

ESQUEMA = """
CREATE TABLE IF NOT EXISTS pedidos (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    dia         TEXT NOT NULL,           -- 'AAAA-MM-DD'
    cliente     TEXT NOT NULL,
    cep         TEXT NOT NULL,
    numero      TEXT,
    logradouro  TEXT,
    bairro      TEXT,
    lat         REAL,
    lon         REAL,
    valido      INTEGER NOT NULL         -- 1 = CEP válido, 0 = inválido
);

CREATE TABLE IF NOT EXISTS rotas (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    dia            TEXT NOT NULL,
    metodo         TEXT NOT NULL,        -- 'força bruta' ou 'vizinho mais próximo'
    n_paradas      INTEGER NOT NULL,
    rotas_testadas INTEGER,
    km_original    REAL NOT NULL,
    km_otimizada   REAL NOT NULL,
    ordem          TEXT NOT NULL         -- ex.: '0,3,1,2'
);

-- cache do Nominatim: não geocodificar o mesmo endereço duas vezes
CREATE TABLE IF NOT EXISTS geocache (
    chave TEXT PRIMARY KEY,              -- 'cep|numero'
    lat   REAL,
    lon   REAL
);
"""


def conectar(caminho: Path | None = None) -> sqlite3.Connection:
    """Abre o banco e cria as tabelas se não existirem. Já pronto.

    Nos testes, passe outro caminho (ou ":memory:") para não sujar o banco de verdade.
    """
    con = sqlite3.connect(caminho or CAMINHO_BANCO)
    con.executescript(ESQUEMA)
    return con


def salvar_rota(con: sqlite3.Connection, dia: str, resultado: dict, km_original: float) -> None:
    """Grava um cálculo de rota (o dict de rota.otimizar) na tabela `rotas`.

    TODO: INSERT com placeholders (?): nunca monte SQL com f-string.
    A ordem vira texto com ",".join(map(str, ordem)). Não esqueça con.commit().
    """
    raise NotImplementedError("banco.salvar_rota")


def historico_diario(con: sqlite3.Connection) -> pd.DataFrame:
    """km por dia, para o gráfico do histórico.

    TODO: pd.read_sql_query com
        SELECT dia, SUM(km_original) AS km_original, SUM(km_otimizada) AS km
        FROM rotas GROUP BY dia ORDER BY dia
    """
    raise NotImplementedError("banco.historico_diario")
