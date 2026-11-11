"""Funções de distância: Haversine e matriz de distâncias entre as paradas."""

import math

import pandas as pd

RAIO_TERRA_KM = 6371


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Distância em km entre dois pontos da superfície da Terra.

    d = 2R · arcsin( √( sin²(Δφ/2) + cos φ1 · cos φ2 · sin²(Δλ/2) ) )

    φ = latitude, λ = longitude, ambas em RADIANOS.

    TODO:
    - converta graus → radianos com math.radians
    - Δφ = φ2 − φ1 e Δλ = λ2 − λ1
    - aplique a fórmula (math.sin, math.cos, math.asin, math.sqrt)
    Teste em tests/test_distancias.py.
    """
    raise NotImplementedError("distancias.haversine")


def matriz_distancias(paradas: pd.DataFrame) -> pd.DataFrame:
    """Matriz n×n com a distância (km) entre cada par de paradas.

    Recebe um DataFrame com as colunas 'nome', 'lat', 'lon' (linha 0 = loja).
    Devolve um DataFrame com index e colunas = nomes das paradas.

    TODO:
    - dois laços (i, j) chamando haversine
    - repare: a matriz é simétrica (d[i][j] = d[j][i]) e a diagonal é 0.
      Dá para calcular só metade. Bom ponto para a apresentação.
    """
    raise NotImplementedError("distancias.matriz_distancias")
