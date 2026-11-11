"""Gráficos com matplotlib. Cada função devolve uma Figure para o app mostrar com st.pyplot(fig)."""

import matplotlib.pyplot as plt
import pandas as pd


def crescimento_fatorial(ate: int = 12, n_atual: int | None = None):
    """Gráfico de n! para n = 1..ate, destacando o n da entrega atual.

    TODO:
    - x = range(1, ate + 1), y = math.factorial(x)
    - use escala log no eixo y (ax.set_yscale("log")), senão só aparecem os últimos pontos
    - desenhe uma linha horizontal em ~1e6 com o rótulo "limite prático"
    """
    raise NotImplementedError("graficos.crescimento_fatorial")


def comparativo_rotas(km_original: float, km_otimizada: float, km_vizinho: float | None = None):
    """Barras: ordem original × força bruta × vizinho mais próximo (km).

    TODO: ax.bar com os valores e o rótulo de cada barra (ax.bar_label).
    """
    raise NotImplementedError("graficos.comparativo_rotas")


def historico_km(historico: pd.DataFrame):
    """Linha ou barras com os km por dia, a partir do DataFrame de banco.historico_diario().

    TODO: colunas 'dia' e 'km'. Compare km_original × km_otimizada para mostrar a economia.
    """
    raise NotImplementedError("graficos.historico_km")
