import pandas as pd
import numpy as np
rodadas = np.arange(1,4,1)
df = pd.DataFrame()

for rodada in rodadas:
    rodada = pd.read_csv(f"https://raw.githubusercontent.com/henriquepgomide/caRtola/master/data/2019/rodada-{rodada}.csv",
                         encoding='utf-8')
    df = pd.concat([df, rodada])

df = df.drop(["atletas.foto","atletas.slug", "atletas.nome" , "Unnamed: 0"], axis=1)

lista_cols_rename = list(df.columns[(df.columns.str.contains("atletas"))])

for col in lista_cols_rename:
    df = df.rename(columns={col : col.replace("atletas.", '')})

df = df.sort_values(["clube_id","atleta_id", "rodada_id"])

df = df[df["clube.id.full.name"] == "Botafogo"]

df["flag_jogou"] = np.where((df["variacao_num"] != 0),1,0)

df = df.query("flag_jogou == 1")

df = df.fillna(0)



def fig(df):
    fig = go.Figure(go.Bar(x=x, y=df.query("posicao_id == 'mei'").groupby("rodada_id")["pontos_num"].sum(), name='mei'))

    fig.add_trace(go.Bar(x=x, y=df.query("posicao_id == 'ata'").groupby("rodada_id")["pontos_num"].sum(), name='ata'))
    fig.add_trace(go.Bar(x=x, y=df.query("posicao_id == 'lat'").groupby("rodada_id")["pontos_num"].sum(), name='lat'))
    fig.add_trace(go.Bar(x=x, y=df.query("posicao_id == 'gol'").groupby("rodada_id")["pontos_num"].sum(), name='gol'))
    fig.add_trace(go.Bar(x=x, y=df.query("posicao_id == 'tec'").groupby("rodada_id")["pontos_num"].sum(), name='tec'))
    fig.add_trace(go.Bar(x=x, y=df.query("posicao_id == 'zag'").groupby("rodada_id")["pontos_num"].sum(), name='zag'))


    fig.update_layout(barmode='group', 
        xaxis={'categoryorder':'total descending'},
        title='Pontuação dos jogadores do Botafogo no Cartola 2019, por posição, por rodada',
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='Pontos por rodada',
            titlefont_size=16,
            tickfont_size=14),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'),
    #     barmode='group',
        bargap=0.15, # gap between bars of adjacent location coordinates.
        bargroupgap=0.1 # gap between bars of the same location coordinate.
    )
    return fig
    
    
    
    
import plotly.graph_objects as go

x = df['rodada_id'].unique()

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])

application = app.server

app.layout = dbc.Container([html.Br(),
                           html.Br(),
    dcc.Markdown('''

# Trabalho final da disciplina de Cloud

** Aluno - Leonardo Viggiano | RM 338948 ** 

# Introdução

O objetivo desta página é demonstrar os desafios e sucessos para
apresentar um Dashboard em HTML com o uso das seguintes ferramentas:

* AWS
  * EC2 Instances
  * Elastic Beanstalk
  * CodePipeline / CodeCommit
* Python
  * Lib Dash
---
'''),
       dcc.Markdown('''

### Passo a passo

** 0 - Criação do repositório no AWS Commit com o código gerador do 
dashboard: **

* O código da apliação em dash pode ser encontrado
[aqui](https://github.com/viggiano75/fiap_cloud)

** 1 - 1º Deploy: VM da AWS a partir do EC2 **

* O primeiro deploy foi feito seguindo os steps de _"Deploy em uma VM no EC2"_
dentro do _lab06_.

* A instância foi criada para teste do código e 
verificação dos requisitos.

** 2 - Deploy:  Usando o Elastic Beanstalk **

* Deploy feito seguindo os steps de _"Deploy na AWS"_ dentro do _lab06_. 

** 3 - Deploy: Usando o CodePipeline **

* Ao tentar fazer o deploy com o CodePipeline, verifiquei que existem 
restrições nas permissões das contas _student_, conforme comunicado 
ao professor. Dessa forma, não foi possível realizar a conexão do CodePipeline
com o GitHub. Como alternativa, os códigos foram colocados no CodeCommit, 
repositório da própria AWS.

** 4 - Criação do repositório no CodeCommit **

* Criação do repositório com os arquivos necessários para a aplicação.

** 5 - Criação do Pipeline no AWS CodePipeline **

* Nesta etapa, foi necessário usar o AWS CodePipeline com a opção de 
_"Use o AWS CodePipeLine para verificar alterações periodicamente"_. Esta foi
a única alternativa que permitiu deploy em pipeline com as permissões
autorizadas nas contas _student_.

* Concluindo, com esse método, o Pipeline verifica atualizações dentro do
repositório do CodeCommit e atualiza a apliação conforme
as alterações são realizadas.

---
'''),                      
    dcc.Markdown('''

### Apresentação do Dashboard

O Dashboard tem como objetivo apenas demonstrar o deploy de uma apliação 
simples, em Python. Ele consiste em apenas um gráfico, com um Dropdown que
permite seleção de filtros.


* Base de dados
  * Os dados foram obtidos neste [GitHub](https://github.com/henriquepgomide/caRtola/tree/master/data) e são
referentes ao CartolaFC (Fantasy Game do Campeonato Brasileiro)
  * Foram feitos alguns tratamentos nos dados para puxar as informações
    de todas as rodadas do Campeonato de 2019, apenas para jogadores que 
    atuaram em partidas. Também foram filtrados apenas jogadores do Botafogo FR).
* Gráfico
  * O gráfico apresenta a soma de pontos de cada categoria de jogador, 
  por rodada.
* Dropdown
  * No dropdown é possível filtrar os dados de forma a selecionar apenas a
  categoria de jogador desejada.
  
---

### Dashboard (plotly Dash)

'''),
                            

                            
                           
    dcc.Graph(id="main-graph", figure=fig(df)),                                        
    dcc.Dropdown(
        id="col-dropdown",
        options=[
            {'label': 'Atacantes' , 'value': 'ata'},
            {'label': 'Meias'     , 'value': 'mei'},
            {'label': 'Laterais'  , 'value': 'lat'},
            {'label': 'Zagueiros' , 'value': 'zag'},
            {'label': 'Goleiro'   , 'value': 'gol'},
            {'label': 'Tecnico'   , 'value': 'tec'}           
        ],
        multi=True,
        value="ata",
        style={'width': '200px'}),
                                                        
html.Br(),
html.Br(),
html.Br(),
html.Br(),
])

@app.callback(
    Output('main-graph', 'figure'),
    [Input('col-dropdown', 'value')]
)

def update_fig(jogador):
    dff = df.copy()
    dff = dff.query("posicao_id == @jogador")
    new_fig = fig(dff)
    return new_fig

########### Run the app
if __name__ == '__main__':
    application.run(debug=False, port=8080, use_reloader=False)
