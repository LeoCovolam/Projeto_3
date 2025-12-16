from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

def cria_graficos(selecao_marcas):

    filtro_df = df[df['Marca'].isin(selecao_marcas)]
    agrupado = filtro_df.groupby(["Gênero", "Preço", "Temporada", "Marca", "N_Avaliações_MinMax", "Nota_MinMax", "Material_Cod"])["Qtd_Vendidos_Cod"].sum().reset_index()

    # Gráfico de Barra
    fig = px.bar(agrupado, x='Gênero', y='Qtd_Vendidos_Cod', text='Qtd_Vendidos_Cod', color='Marca', barmode='group', color_discrete_sequence=px.colors.qualitative.Bold, opacity=1)
    fig.update_layout(
        title='TOP 10 Marcas Mais Vendidas',
        xaxis_title='Gênero',
        yaxis_title='Quantidade Vendida',
        legend_title='Marca',
        plot_bgcolor='rgba(222, 255, 253, 1)',  # Fundo Interno
        paper_bgcolor='rgba(186, 245, 241, 1)'  # Fundo Externo
    )

    # Gráfico de Dispersão
    fig1 = px.scatter(agrupado, x='Marca', y='Preço', color='Gênero', hover_data=['Temporada'])
    fig1.update_layout(
        title='Preço vs Marca por Gênero',
        xaxis_title='Marca',
        yaxis_title='Preço'
    )

    # Gráfico de Bolha
    fig2 = px.scatter(agrupado, x='N_Avaliações_MinMax', y='Nota_MinMax', size='Preço', color='Marca', hover_name='Material_Cod', size_max=60)
    fig2.update_layout(
        title='Avaliações por Nota e Preço',
        xaxis_title='Avaliações',
        yaxis_title='Nota'
    )
    return fig, fig1, fig2

def cria_app():
    # cria App
    app = Dash(__name__)

    app.layout = html.Div([
        html.H1('Dashboard Interativo'),
        html.Div('''
        Interatividade entre os
        dados.
        '''),
        html.Br(),
        html.H2('TOP 10 MARCAS'),
        dcc.Checklist(
            id='id_selecao_marcas',
            options=options,
            value=[lista_top10_marcas[0]],
        ),
        dcc.Graph(id='id_grafico_barra'),
        dcc.Graph(id='id_grafico_dispersao'),
        dcc.Graph(id='id_grafico_bolhas')

    ])
    return app

df = pd.read_csv("C:/Users/Elaine Alcantara/OneDrive - Ilumitech/Desktop/Analista de Dados/ecommerce_estatistica.csv")
top10 = df.groupby("Marca")["Qtd_Vendidos_Cod"].sum().nlargest(10).reset_index()
lista_top10_marcas = top10["Marca"].unique()
options = [{'label': marca, 'value': marca} for marca in lista_top10_marcas]

# Execute App
if __name__ == '__main__':
    app = cria_app()

    @app.callback(
               [
            Output('id_grafico_barra', "figure"),
            Output('id_grafico_dispersao', "figure"),
            Output('id_grafico_bolhas', "figure")
        ],
        [Input('id_selecao_marcas', 'value')]
    )
    def atualiza_grafico(selecao_marcas):
        fig, fig1, fig2 = cria_graficos(selecao_marcas)
        return [fig, fig1, fig2]
    app.run(debug=True, port=8051)  # Default 8051
