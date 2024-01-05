from bs4 import BeautifulSoup
from dash import Dash, html, dcc, Output, Input
import plotly.graph_objects as go
import pandas as pd
import yfinance as yf
from datetime import datetime
import requests

cotacoes = ['PETR4.SA', 'WEGE3.SA', 'CEAB3.SA']
tickers_sem_suffix = [ticker.replace('.SA', '') for ticker in cotacoes]

app = Dash(__name__)

selected_ticker = None

app.layout = html.Div(
    children=[
        dcc.Dropdown(
            options=[{'label': cotacoes, 'value': ticker} for ticker, cotacoes in zip(cotacoes, tickers_sem_suffix)],
            value='PETR4.SA', id='dropdown', style={'width': '50%', 'margin': 'auto', 'marginTop': 0, 'font-family': 'Lato', 'background-color': 'white'}
        ),
        dcc.Graph(id='graph-content', className='my-graph-style', style={'background-color': '#131516'}),
        html.Div(id='info-content', className='my-info-style', style={'background-color': '#131516'}),
        html.H1('Notícias', style={'position': 'absolute', 'top': '-45px', 'left': '130%', 'font-size': '46px', 'background-color': 'white'}),
        html.Div(id='noticias-div', style={'position': 'absolute', 'top': '100px', 'width': '80%', 'margin': 'auto', 'left': '100%', 'font-family': 'Lato', 'background-color': 'white'})
    ],
    style={'width': '50%', 'margin': 'auto', 'background-color': 'white', 'position': 'absolute', 'left': '0', 'top': '20%', 'height': '80vh', 'color': 'black', 'font-family': 'Lato'}
)

@app.callback(
    [Output('graph-content', 'figure'),
     Output('info-content', 'children'),
     Output('noticias-div', 'children')],
    Input('dropdown', 'value')
)
def update_graph(selected_ticker_input):
    global selected_ticker

    try:
        if selected_ticker_input is None:
            return go.Figure(), None, None
        
        elif selected_ticker_input == 'WEGE3.SA':
            response = requests.get('https://braziljournal.com/?s=weg')

        elif selected_ticker_input == 'PETR4.SA':
            response = requests.get('https://braziljournal.com/?s=petrobras')

        elif selected_ticker_input == 'CEAB3.SA':
            response = requests.get('https://braziljournal.com/?s=c%26a')

        soup = BeautifulSoup(response.text, 'html.parser')
        ws = soup.select('.boxarticle-infos a')
        
        titles = []

        texto1 = ws[0].text.strip()
        link1 = ws[1]['href'] if 'href' in ws[0].attrs else '#'
        texto2 = ws[1].text.strip()
        link2 = ws[1]['href'] if 'href' in ws[1].attrs else '#'

        texto3 = ws[2].text.strip()
        link3 = ws[3]['href'] if 'href' in ws[2].attrs else '#'
        texto4 = ws[3].text.strip()
        link4 = ws[3]['href'] if 'href' in ws[3].attrs else '#'

        texto5 = ws[4].text.strip()
        link5 = ws[5]['href'] if 'href' in ws[4].attrs else '#'
        texto6 = ws[5].text.strip()
        link6 = ws[5]['href'] if 'href' in ws[5].attrs else '#'

        titles = [
            html.P(html.A(texto1, href=link1, target='_blank', style={'text-decoration': 'none', 'font-family': 'Lato', 'color': '#949daf', 'font-size': '18px'})),
            html.P(html.A(texto2, href=link2, target='_blank', style={'text-decoration': 'none', 'font-family': 'Lato', 'color': 'black', 'font-size': '18px'})),
            html.P(html.A(texto3, href=link3, target='_blank', style={'text-decoration': 'none', 'font-family': 'Lato', 'color': '#949daf', 'font-size': '18px'})),
            html.P(html.A(texto4, href=link4, target='_blank', style={'text-decoration': 'none', 'font-family': 'Lato', 'color': 'black', 'font-size': '18px'})),
            html.P(html.A(texto5, href=link5, target='_blank', style={'text-decoration': 'none', 'font-family': 'Lato', 'color': '#949daf', 'font-size': '18px'})),
            html.P(html.A(texto6, href=link6, target='_blank', style={'text-decoration': 'none', 'font-family': 'Lato', 'color': 'black', 'font-size': '18px'}))
        ]

        selected_ticker = selected_ticker_input

        data = yf.download(selected_ticker, '2023-01-01', datetime.now())
        df = pd.DataFrame(data, columns=['Open', 'High', 'Low', 'Close']).dropna()

        fig = go.Figure(data=[go.Candlestick(x=df.index,
                                             open=df['Open'],
                                             high=df['High'],
                                             low=df['Low'],
                                             close=df['Close'],
                                             increasing=dict(line=dict(color='green')),
                                             decreasing=dict(line=dict(color='red'))
                                            )])

        fig.update_layout(xaxis_rangeslider_visible=False)
        fig.update_xaxes(title_text='')
        fig.update_yaxes(title_text='')

        return fig, None, titles

    except Exception as e:
        error_message = f"Error: {e}"
        return go.Figure(), error_message, None

if __name__ == '__main__':
    app.run_server(debug=True)
