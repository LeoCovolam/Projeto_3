# 📦 Importação de bibliotecas
import plotly.express as px        # Biblioteca para criar gráficos interativos
import pandas as pd                # Biblioteca para manipulação de dados
from dash import Dash, html, dcc   # Componentes principais do framework Dash


# 📊 Função que cria os gráficos com base no DataFrame
def cria_graficos(df):
    # 📈 Gráfico 1: Histograma da distribuição das notas dos produtos
    fig1 = px.histogram(df, x='Nota', nbins=35, title='Distribuição das Notas dos Produtos')
    fig1.update_traces(marker_color='purple', marker_line_width=1, marker_line_color="black")
    fig1.update_layout(
        yaxis_title='Frequência',
        title_x=0.5,
        width=800,
        height=500
    )

    # 🔵 Gráfico 2: Dispersão entre nota e número de avaliações
    fig2 = px.scatter(df, x='Nota', y='N_Avaliações')
    fig2.update_traces(marker_color='green')
    fig2.update_layout(
        title='Dispersão - Relação entre Notas e Número de avaliações',
        yaxis_title='Número de Avaliações',
        title_x=0.5,
        width=800,
        height=500
    )

    # 🔥 Gráfico 3: Mapa de calor de correlação entre variáveis numéricas
    df_corr = df[['Nota', 'N_Avaliações', 'Desconto', 'Preço', 'Qtd_Vendidos_Cod']].corr()
    fig3 = px.imshow(df_corr, text_auto=True, aspect='auto', color_continuous_scale='thermal',
                     title='Mapa de Calor de Correlação entre Variáveis')
    fig3.update_layout(
        title_x=0.5,
        width=800,
        height=500
    )

    # 📦 Gráfico 4: Barras com total de vendas por marca (agrupando "Outros")
    vendas_por_marca = df.groupby('Marca')['Qtd_Vendidos_Cod'].sum()

    # Define marcas "relevantes" como aquelas com pelo menos 2% das vendas totais
    threshold = 0.02 * vendas_por_marca.sum()
    marcas_relevantes = vendas_por_marca[vendas_por_marca >= threshold]
    outros = vendas_por_marca[vendas_por_marca < threshold].sum()

    # Adiciona "Outros" caso existam marcas irrelevantes
    if outros > 0:
        marcas_relevantes = pd.concat([marcas_relevantes, pd.Series({'Outros': outros})])

    # Dados para os gráficos de barras e pizza
    x = marcas_relevantes.index
    y = marcas_relevantes.values

    # 📊 Gráfico 5: Barras com vendas por marca
    fig4 = px.bar(x=x, y=y)
    fig4.update_traces(marker_color='orange', marker_line_width=1, marker_line_color="black")
    fig4.update_layout(
        title='Vendas por Marca',
        title_x=0.5,
        xaxis_title='Marca',
        yaxis_title='Quantidade de Vendas',
        width=800,
        height=500
    )

    # 🥧 Gráfico 6: Gráfico de pizza com distribuição percentual de vendas por marca
    fig5 = px.pie(
        values=y,
        names=x,
        hole=0.2,
        title='Distribuição de Vendas por Marca',
        color_discrete_sequence=px.colors.sequential.GnBu
    )
    fig5.update_traces(textinfo='percent+label', marker=dict(line=dict(color='black', width=1)))
    fig5.update_layout(
        title_x=0.5,
        width=800,
        height=500
    )

    # 📉 Gráfico 7: Contorno de densidade para a variável "Preço"
    fig6 = px.density_contour(df, x='Preço')
    fig6.update_traces(contours_coloring="fill", contours_showlabels=True)
    fig6.update_layout(
        xaxis_title='Preço R$',
        title='Densidade de Preços',
        title_x=0.5,
        width=800,
        height=500
    )

    # Retorna todos os gráficos
    return fig1, fig2, fig3, fig4, fig5, fig6

# 🧩 Função que cria a aplicação Dash
def cria_app(df):
    app = Dash(__name__)  # Inicializa o app Dash

    # Gera os gráficos a partir do DataFrame
    fig1, fig2, fig3, fig4, fig5, fig6, = cria_graficos(df)

    # Define o layout do dashboard, com todos os gráficos incluídos
    app.layout = html.Div([
        html.H1('Dashboard para visualização de gráficos'),  # Título principal
        dcc.Graph(figure=fig1),
        dcc.Graph(figure=fig2),
        dcc.Graph(figure=fig3),
        dcc.Graph(figure=fig4),
        dcc.Graph(figure=fig5),
        dcc.Graph(figure=fig6)
    ])

    return app  # Retorna o app

# 📁 Carregamento dos dados do arquivo CSV
df = pd.read_csv("C:/Users/Elaine Alcantara/OneDrive - Ilumitech/Desktop/Analista de Dados/ecommerce_estatistica.csv")

# 🚀 Execução do app
if __name__ == '__main__':
    app = cria_app(df)           # Cria o app
    app.run(debug=True, port=8050)  # Inicia o servidor local na porta 8050



