"""Gabarito do Haversine. Rode com: pytest"""

import pandas as pd
import pytest

from rotacerta.distancias import haversine, matriz_distancias


def test_mesmo_ponto_da_zero():
    assert haversine(-25.43, -49.27, -25.43, -49.27) == pytest.approx(0)


def test_um_grau_de_latitude_da_111_km():
    # um grau no meridiano = 2πR / 360 ≈ 111,19 km
    assert haversine(0, 0, 1, 0) == pytest.approx(111.19, abs=0.01)


def test_e_simetrica():
    a = haversine(-25.4284, -49.2733, -25.4411, -49.2900)
    b = haversine(-25.4411, -49.2900, -25.4284, -49.2733)
    assert a == pytest.approx(b)


def test_matriz_simetrica_com_diagonal_zero():
    paradas = pd.DataFrame({"nome": ["loja", "a", "b"],
                            "lat": [-25.43, -25.44, -25.45], "lon": [-49.27, -49.28, -49.26]})
    m = matriz_distancias(paradas)
    assert m.shape == (3, 3)
    for i in range(3):
        assert m.iat[i, i] == 0
        for j in range(3):
            assert m.iat[i, j] == pytest.approx(m.iat[j, i])
