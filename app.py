"""RotaCerta: interface Streamlit.

Rodar: streamlit run app.py

Este arquivo só monta a tela e chama as funções de rotacerta/. A matemática fica lá.
Enquanto uma função estiver com TODO, a etapa mostra um aviso e as que dependem dela param.
"""

from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd
import streamlit as st

from rotacerta import apis, banco, distancias, graficos, mapa, rota

EXEMPLO = Path(__file__).parent / "dados" / "pedidos_exemplo.csv"

st.set_page_config(page_title="RotaCerta", page_icon="🛵", layout="wide")


def etapa(nome: str, fn, *args, **kwargs):
    """Roda fn. Se ainda não foi implementada, avisa na tela e devolve None."""
    try:
        return fn(*args, **kwargs)
    except NotImplementedError as e:
        st.info(f"**{nome}**: falta implementar `{e}`.")
        return None


# chamadas de API com cache: o mesmo CEP não é consultado duas vezes na sessão
buscar_cep = st.cache_data(apis.buscar_cep)
geocodificar = st.cache_data(apis.geocodificar)
clima_na_hora = st.cache_data(apis.clima_na_hora)


def proxima_hora(hora: datetime, km_trecho: float) -> datetime:
    """Horário de chegada na próxima parada: deslocamento + tempo da entrega."""
    try:
        return hora + timedelta(minutes=rota.tempo_estimado(km_trecho, 1))
    except NotImplementedError:
        return hora  # sem tempo_estimado, todas as paradas ficam no horário de saída


# ---------- barra lateral ----------
with st.sidebar:
    st.title("🛵 RotaCerta")
    dia = st.date_input("Dia das entregas", date.today())
    saida = st.time_input("Horário de saída", datetime.strptime("14:00", "%H:%M").time())
    voltar = st.checkbox("Voltar para a loja no fim", value=False)
    arquivo = st.file_uploader("Pedidos (CSV)", type="csv")
    st.caption("Colunas: tipo (loja/pedido), cliente, cep, numero. Sem arquivo, usa o exemplo.")


def aba_rota(pedidos: pd.DataFrame) -> None:
    st.subheader("1. Pedidos")
    pedidos = st.data_editor(pedidos, num_rows="dynamic", width="stretch")

    # session_state: o resultado continua na tela quando você mexe no mapa (o Streamlit reroda tudo)
    if st.button("Calcular rota", type="primary"):
        st.session_state.calcular = True
    if not st.session_state.get("calcular"):
        return

    # 2. validação de CEP (conjuntos)
    st.subheader("2. Validação dos CEPs")
    separados = etapa("Separar CEPs", apis.separar_ceps, list(pedidos["cep"]))
    if separados is None:
        return
    validos, invalidos = separados
    c1, c2 = st.columns(2)
    c1.metric("CEPs válidos", len(validos))
    c2.metric("CEPs inválidos", len(invalidos))
    if invalidos:
        st.warning("Inválidos (fora da rota): " + ", ".join(sorted(invalidos)))

    # 3. geocodificação: monta o DataFrame de paradas (linha 0 = loja)
    st.subheader("3. Paradas")
    pedidos = pedidos.assign(cep_limpo=pedidos["cep"].map(apis.limpar_cep))
    pedidos = pedidos[pedidos["cep_limpo"].isin(validos)]
    pedidos = pd.concat([pedidos[pedidos["tipo"] == "loja"], pedidos[pedidos["tipo"] != "loja"]])
    linhas = []
    for _, p in pedidos.iterrows():
        endereco = etapa("Buscar CEP", buscar_cep, p["cep_limpo"])
        coords = endereco and etapa("Geocodificar", geocodificar, endereco, p["numero"])
        if not coords:
            if endereco:
                st.warning(f"Não achei as coordenadas de {p['cliente']}.")
            return
        linhas.append({"nome": p["cliente"], "endereco": f'{endereco["logradouro"]}, {p["numero"]}',
                       "bairro": endereco["bairro"], "lat": coords[0], "lon": coords[1]})
    paradas = pd.DataFrame(linhas)
    st.dataframe(paradas, width="stretch")

    # 4. matriz de distâncias (Haversine)
    st.subheader("4. Matriz de distâncias (km)")
    st.latex(r"d = 2R \arcsin\left(\sqrt{\sin^2\left(\tfrac{\Delta\varphi}{2}\right)"
             r" + \cos\varphi_1 \cos\varphi_2 \sin^2\left(\tfrac{\Delta\lambda}{2}\right)}\right)")
    dist = etapa("Matriz de distâncias", distancias.matriz_distancias, paradas)
    if dist is None:
        return
    st.dataframe(dist.round(2), width="stretch")

    # 5. otimização
    st.subheader("5. Rota otimizada")
    n = len(paradas) - 1
    st.latex(rf"R({n}) = {n}! = {rota.numero_de_rotas(n):,}".replace(",", "."))
    ordem_original = list(range(1, n + 1))
    km_original = etapa("Custo da rota", rota.custo_rota, ordem_original, dist, voltar)
    resultado = etapa("Otimizar", rota.otimizar, dist, voltar)
    if km_original is None or resultado is None:
        return

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Ordem original", f"{km_original:.1f} km")
    c2.metric(f"Otimizada ({resultado['metodo']})", f"{resultado['km']:.1f} km",
              f"{resultado['km'] - km_original:.1f} km", delta_color="inverse")
    c3.metric("Vizinho mais próximo", f"{resultado['vizinho_km']:.1f} km")
    testadas = resultado["rotas_testadas"]
    c4.metric("Rotas testadas", f"{testadas:,}".replace(",", ".") if testadas else "heurística")
    t_orig = etapa("Tempo estimado", rota.tempo_estimado, km_original, n)
    t_otim = etapa("Tempo estimado", rota.tempo_estimado, resultado["km"], n)
    if t_orig is not None and t_otim is not None:
        st.success(f"Economia estimada: **{t_orig - t_otim:.0f} min** ({t_otim:.0f} min no total)")

    # 6. mapa
    st.subheader("6. Mapa")
    m = etapa("Mapa", mapa.desenhar_rota, paradas, resultado["ordem"])
    if m is not None:
        from streamlit_folium import st_folium
        st_folium(m, height=450, use_container_width=True)

    # 7. roteiro com horário previsto e clima de cada parada
    st.subheader("7. Roteiro e clima")
    caminho = [0] + resultado["ordem"]
    hora = datetime.combine(dia, saida)
    linhas = []
    for k, i in enumerate(caminho):
        if k > 0:
            hora = proxima_hora(hora, dist.iat[caminho[k - 1], i])
        p = paradas.iloc[i]
        c = etapa("Clima", clima_na_hora, p["lat"], p["lon"], hora.strftime("%Y-%m-%dT%H:00"))
        linhas.append({"visita": k, "nome": p["nome"], "endereco": p["endereco"], "bairro": p["bairro"],
                       "horário": hora.strftime("%H:%M"),
                       "°C": c["temperatura"] if c else None, "chuva %": c["chuva_pct"] if c else None})
    roteiro = pd.DataFrame(linhas)
    st.dataframe(roteiro, width="stretch")

    # 8. gráfico comparativo, salvar, exportar
    fig = etapa("Gráfico comparativo", graficos.comparativo_rotas,
                km_original, resultado["km"], resultado["vizinho_km"])
    if fig is not None:
        st.pyplot(fig)

    with banco.conectar() as con:
        etapa("Salvar rota", banco.salvar_rota, con, dia.isoformat(), resultado, km_original)

    st.download_button("Exportar rota (CSV)", roteiro.to_csv(index=False).encode("utf-8"),
                       file_name=f"rota-{dia.isoformat()}.csv", mime="text/csv")


def aba_fatorial(n_atual: int) -> None:
    st.subheader("Por que a força bruta deixa de ser viável")
    st.latex(r"R(n) = n! = n \cdot (n-1) \cdot (n-2) \cdots 1")
    st.table(pd.DataFrame({
        "paradas (n)": range(1, 13),
        "rotas (n!)": [f"{rota.numero_de_rotas(k):,}".replace(",", ".") for k in range(1, 13)],
    }))
    fig = etapa("Gráfico de n!", graficos.crescimento_fatorial, 12, n_atual)
    if fig is not None:
        st.pyplot(fig)


def aba_historico() -> None:
    st.subheader("Histórico de entregas")
    with banco.conectar() as con:
        hist = etapa("Histórico", banco.historico_diario, con)
    if hist is None:
        return
    if hist.empty:
        st.caption("Nenhuma rota salva ainda.")
        return
    st.dataframe(hist, width="stretch")
    fig = etapa("Gráfico do histórico", graficos.historico_km, hist)
    if fig is not None:
        st.pyplot(fig)


pedidos = pd.read_csv(arquivo or EXEMPLO, dtype=str)
t_rota, t_fatorial, t_hist = st.tabs(["Rota do dia", "Por que n! explode", "Histórico"])
with t_rota:
    aba_rota(pedidos)
with t_fatorial:
    aba_fatorial(n_atual=int((pedidos["tipo"] != "loja").sum()))
with t_hist:
    aba_historico()
