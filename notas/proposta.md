# Proposta A3 — RotaCerta: Painel de Entregas com CEP, Clima e Rota Otimizada

Oct 28, 2026 · @Yan

## Identificação

- **Disciplina:** Matemática Computacional Aplicada
- **Professores:** Aron e Cristiano
- **Integrantes:** Nome: Yan Machado Nunes RA: 172513312, Nome: Maycon da Silva Pereira RA: 942622071
- **Tema:** baseado na sugestão (b) "Painel de apoio a entregas com CEP e clima", ampliado com otimização de rota

## Nome do projeto

**RotaCerta** — painel web que organiza as entregas do dia de um pequeno comércio: valida endereços por CEP, mostra o clima de cada parada e calcula a ordem de visita mais curta.

## Problema real

Pequenos comércios que fazem entregas próprias (farmácias de bairro, padarias, floriculturas, lojas de material) montam a rota "de cabeça" ou na ordem em que os pedidos chegaram. Isso gera quilômetros a mais, atrasos e combustível desperdiçado.

Além disso, o entregador não sabe com antecedência se vai pegar chuva em algum trecho, o que afeta entregas de moto e produtos sensíveis. Endereços digitados errado também causam viagens perdidas.

## Público-alvo

- Donos e atendentes de pequenos comércios com entrega própria, sem acesso a sistemas de roteirização pagos
- Entregadores autônomos (motoboys, ciclistas) que fazem várias paradas por dia
- Microempreendedores que vendem por WhatsApp ou Instagram e entregam pessoalmente

## Solução proposta

O usuário cadastra o ponto de partida (a loja) e os pedidos do dia informando o CEP e o número. O RotaCerta faz o resto em quatro etapas:

1. **Validação de endereços:** consulta cada CEP na API pública ViaCEP e completa rua, bairro e cidade. CEPs inválidos são sinalizados.
2. **Localização e distâncias:** converte os endereços em coordenadas (latitude e longitude) e monta a matriz de distâncias entre todas as paradas pela fórmula de Haversine.
3. **Rota otimizada:** testa todas as permutações possíveis da ordem de visita (força bruta) e escolhe a de menor distância total. Acima de 9 paradas, usa a heurística do vizinho mais próximo e compara o resultado.
4. **Clima por parada:** consulta a API Open-Meteo e mostra temperatura e chance de chuva no horário previsto de cada entrega.

**Funcionalidades da interface:**

- Mapa com as paradas numeradas e a rota desenhada
- Comparativo "ordem original × rota otimizada" em km e minutos economizados
- Gráfico do crescimento de n! mostrando por que a força bruta deixa de ser viável
- Exibição da fórmula e do número de rotas testadas em cada cálculo
- Histórico de entregas salvo em banco de dados, com gráficos de km por dia
- Exportação da rota em CSV para o entregador

## Conteúdos da disciplina aplicados

O projeto aplica sete conteúdos da disciplina, acima do mínimo de três exigido.

| Conteúdo | Onde aparece no projeto |
| --- | --- |
| Permutação e princípio fundamental da contagem | Geração de todas as ordens de visita possíveis; com n paradas existem n! rotas (8 paradas = 40.320 rotas) |
| Funções | Distância de Haversine, custo total de uma rota, tempo estimado de entrega |
| Noção de conjuntos | Separação de CEPs válidos e inválidos, paradas visitadas e não visitadas na heurística |
| Consumo de API pública | ViaCEP (endereços), Open-Meteo (clima) e serviço de geocodificação (coordenadas) |
| DataFrames com Pandas | Tabela de pedidos, matriz de distâncias e histórico de entregas |
| Gráficos com matplotlib | Crescimento de n!, comparativo de km por rota e histórico diário |
| Banco de dados | SQLite com as tabelas de pedidos, rotas calculadas e histórico |

Fórmula de Haversine, usada para a distância entre duas paradas (R = 6.371 km, raio da Terra):

```latex
d = 2R \arcsin\left(\sqrt{\sin^2\left(\frac{\Delta\varphi}{2}\right) + \cos\varphi_1 \cos\varphi_2 \sin^2\left(\frac{\Delta\lambda}{2}\right)}\right)
```

Número de rotas testadas pela força bruta, com a loja fixa como ponto de partida:

```latex
R(n) = n! = n \cdot (n-1) \cdot (n-2) \cdots 1
```

## Tecnologias e dados

| Camada | Tecnologia |
| --- | --- |
| Linguagem | Python 3 |
| Interface web | Streamlit |
| Dados e cálculos | Pandas, itertools (permutações), math |
| Gráficos | matplotlib |
| Mapa | Folium (OpenStreetMap) |
| Banco de dados | SQLite |
| APIs públicas | ViaCEP, Open-Meteo, Nominatim (geocodificação do OpenStreetMap) |
| Versionamento | GitHub, com README de instalação e execução |

**Dados:** os pedidos e clientes serão fictícios, criados pelo grupo. Os CEPs usados serão endereços públicos reais de Curitiba, para que as APIs retornem dados verdadeiros. Nenhum dado pessoal real será armazenado.

## Cronograma

| Etapa | Entrega | Prazo |
| --- | --- | --- |
| Proposta | Este documento | 28/10/2026 |
| Protótipo | Validação de CEP + cálculo da rota otimizada por permutação funcionando na interface | 11/11/2026 |
| Versão final | Clima, mapa, gráficos, banco de dados, histórico e README | 18/11/2026 |
| Amostra da A3 | Pôster com QR Code para o repositório e vídeo de demonstração | 01/12/2026 |
