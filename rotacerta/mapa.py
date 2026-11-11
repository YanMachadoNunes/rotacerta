"""Mapa com Folium (OpenStreetMap)."""

import folium
import pandas as pd

CENTRO_CURITIBA = (-25.4284, -49.2733)


def desenhar_rota(paradas: pd.DataFrame, ordem: list[int]) -> folium.Map:
    """Mapa com as paradas numeradas na ordem de visita e a linha da rota.

    `paradas` tem as colunas 'nome', 'lat', 'lon' (linha 0 = loja).

    TODO:
    - folium.Map(location=CENTRO_CURITIBA, zoom_start=13)
    - marcador da loja com outra cor: folium.Marker(..., icon=folium.Icon(color="red"))
    - para cada parada, um marcador com o número da visita. Dica:
      folium.Marker(..., icon=folium.DivIcon(html=f"<b>{k}</b>"))
    - folium.PolyLine(lista_de_(lat, lon)_na_ordem).add_to(m)
    - m.fit_bounds(...) para enquadrar todas as paradas
    """
    raise NotImplementedError("mapa.desenhar_rota")
