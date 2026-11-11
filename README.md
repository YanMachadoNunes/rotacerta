# RotaCerta

Painel web que organiza as entregas do dia de um pequeno comércio: valida endereços por CEP,
mostra o clima de cada parada e calcula a ordem de visita mais curta.

A3 de **Matemática Computacional Aplicada**, com Yan Machado Nunes e Maycon da Silva Pereira.

## Rodar

```sh
python -m venv .venv
source .venv/bin/activate.fish     # bash/zsh: source .venv/bin/activate
pip install -r requirements.txt

streamlit run app.py               # abre o painel em http://localhost:8501
pytest                             # roda os testes (o "gabarito" das funções)
```

## Estrutura

```
app.py                  interface Streamlit (só chama as funções abaixo)
rotacerta/
  apis.py               ViaCEP, Nominatim, Open-Meteo        → consumo de API
  distancias.py         Haversine + matriz de distâncias      → funções, DataFrame
  rota.py               custo, força bruta, vizinho próximo   → permutação, conjuntos
  graficos.py           n!, comparativo, histórico            → matplotlib
  mapa.py               paradas numeradas + rota (Folium)
  banco.py              SQLite: pedidos, rotas, histórico     → banco de dados
dados/pedidos_exemplo.csv   pedidos fictícios com CEPs reais de Curitiba
tests/                  testes com valores conhecidos
notas/                  proposta e anotações da dupla
```

## Conteúdos da disciplina → onde estão

| Conteúdo | Arquivo |
|---|---|
| Permutação / princípio da contagem | `rota.py` (`forca_bruta`, `numero_de_rotas`) |
| Funções | `distancias.py` (`haversine`), `rota.py` (`custo_rota`, `tempo_estimado`) |
| Conjuntos | `apis.py` (`separar_ceps`), `rota.py` (`vizinho_mais_proximo`) |
| API pública | `apis.py` |
| Pandas | `distancias.py` (`matriz_distancias`), `banco.py` |
| matplotlib | `graficos.py` |
| Banco de dados | `banco.py` |

## Roteiro

**Protótipo (11/11):** CEP + rota por permutação na interface
- [ ] `apis.buscar_cep` e `apis.separar_ceps`
- [ ] `apis.geocodificar`
- [ ] `distancias.haversine` e `distancias.matriz_distancias`
- [ ] `rota.custo_rota` e `rota.forca_bruta`

**Versão final (18/11):**
- [ ] `rota.vizinho_mais_proximo` + comparativo
- [ ] `apis.clima_na_hora` + `rota.tempo_estimado`
- [ ] `mapa.desenhar_rota`
- [ ] `graficos.*`
- [ ] `banco.*` + aba de histórico
- [ ] exportar CSV

**Amostra (01/12):** pôster com QR Code para o repositório + vídeo de demonstração

## Onde parei

- 2026-11-05: esqueleto criado.
