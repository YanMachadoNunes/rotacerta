"""Consumo de APIs públicas: ViaCEP (endereço), Nominatim (coordenadas), Open-Meteo (clima).

Nenhuma delas precisa de chave. Regras de bom uso:
- Nominatim pede no máximo 1 requisição por segundo e um User-Agent que identifique o app.
- Sempre use timeout em requests.get, senão o painel trava se a API cair.
"""

import requests

VIACEP_URL = "https://viacep.com.br/ws/{cep}/json/"
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
USER_AGENT = "RotaCerta/0.1 (trabalho academico A3)"
TIMEOUT = 10


def limpar_cep(cep: str) -> str:
    """'80020-310' → '80020310'. Já pronto: só mantém os dígitos."""
    return "".join(c for c in str(cep) if c.isdigit())


def buscar_cep(cep: str) -> dict | None:
    """Consulta o ViaCEP e devolve {'cep', 'logradouro', 'bairro', 'localidade', 'uf'}.

    Devolve None quando o CEP é inválido.

    TODO:
    - limpe o CEP e confira se tem 8 dígitos (senão já devolve None)
    - faça o GET em VIACEP_URL.format(cep=...)
    - atenção: CEP inexistente NÃO dá erro HTTP. O ViaCEP responde 200 com {"erro": true}
    """
    raise NotImplementedError("apis.buscar_cep")


def separar_ceps(ceps: list[str]) -> tuple[set[str], set[str]]:
    """Noção de conjuntos: separa os CEPs em (validos, invalidos).

    TODO:
    - percorra os CEPs chamando buscar_cep
    - monte os dois conjuntos
    - propriedades que valem conferir (e mostrar na apresentação):
        validos ∩ invalidos = ∅
        validos ∪ invalidos = set(ceps)
    """
    raise NotImplementedError("apis.separar_ceps")


def geocodificar(endereco: dict, numero: str) -> tuple[float, float] | None:
    """Converte endereço em (latitude, longitude) pelo Nominatim.

    TODO:
    - parâmetros: street=f"{numero} {logradouro}", city, state, country="Brasil", format="json", limit=1
    - header: {"User-Agent": USER_AGENT}
    - a resposta é uma lista. Vazia = não achou. Senão use float(r[0]["lat"]) e float(r[0]["lon"])
    - se não achar com o número, tente sem ele (cai no meio da rua, o que basta)
    - respeite 1 req/s: time.sleep(1) entre chamadas (ou guarde o resultado no banco como cache)
    """
    raise NotImplementedError("apis.geocodificar")


def clima_na_hora(lat: float, lon: float, hora_iso: str) -> dict | None:
    """Temperatura e chance de chuva previstas para uma hora (ex.: '2026-11-11T14:00').

    Devolve {'temperatura': float, 'chuva_pct': int} ou None.

    TODO:
    - parâmetros: latitude, longitude, hourly="temperature_2m,precipitation_probability",
      timezone="America/Sao_Paulo"
    - a resposta traz listas paralelas em r["hourly"]: "time", "temperature_2m", ...
    - ache o índice da hora em r["hourly"]["time"] (arredonde a hora para baixo antes de procurar)
    """
    raise NotImplementedError("apis.clima_na_hora")
