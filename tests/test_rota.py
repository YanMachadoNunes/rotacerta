"""Gabarito da otimização com uma matriz pequena, que dá para conferir à mão."""

import pandas as pd
import pytest

from rotacerta.rota import custo_rota, forca_bruta, numero_de_rotas, vizinho_mais_proximo

# loja (0) e 3 paradas numa linha reta: 0 —1km— 1 —1km— 2 —1km— 3
POS = [0, 1, 2, 3]
DIST = pd.DataFrame([[abs(a - b) for b in POS] for a in POS], dtype=float)


def test_numero_de_rotas():
    assert numero_de_rotas(3) == 6
    assert numero_de_rotas(8) == 40320


def test_custo_rota():
    assert custo_rota([1, 2, 3], DIST) == pytest.approx(3)
    assert custo_rota([3, 2, 1], DIST) == pytest.approx(5)  # vai até o fim e volta
    assert custo_rota([1, 2, 3], DIST, voltar_para_loja=True) == pytest.approx(6)


def test_forca_bruta_acha_a_melhor_e_testa_n_fatorial():
    ordem, km, testadas = forca_bruta(DIST)
    assert ordem == [1, 2, 3]
    assert km == pytest.approx(3)
    assert testadas == numero_de_rotas(3)


def test_vizinho_visita_todas_uma_vez():
    ordem, km = vizinho_mais_proximo(DIST)
    assert sorted(ordem) == [1, 2, 3]
    assert km >= forca_bruta(DIST)[1]  # heurística nunca ganha da força bruta
