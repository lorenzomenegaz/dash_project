from dash import Dash, html, dcc, callback, Output, Input
import plotly.graph_objects as go
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

cotacoes = ['PETR4.SA', 'WEGE3.SA', 'CEAB3.SA']

tickers_sem_suffix = [ticker.replace('.SA', '') for ticker in cotacoes]



app = Dash(__name__, external_stylesheets=['style.css'])

selected_ticker = None

app.layout = html.Div(
    children=[
        dcc.Dropdown(
            options=[{'label': cotacoes, 'value': ticker} for ticker, cotacoes in zip(cotacoes, tickers_sem_suffix)],
            value='PETR4.SA', id='dropdown-selection', style={'width': '50%', 'margin': 'auto', 'marginTop': 0, 'font-family': 'Helvetica'}
        ),
        dcc.Graph(id='graph-content', className='my-graph-style'),
        html.Div(id='info-content', className='my-info-style'),
        html.H1('Notícias', style={'position': 'absolute', 'top': '-45px', 'left': '130%', 'font-size': '46px'}),
    ],
    style={'width': '50%', 'margin': 'auto', 'background-color': 'white', 'position': 'absolute', 'left': '0', 'top': '20%', 'height': '60vh', 'color': 'black', 'font-family': 'Helvetica'}
)

@app.callback(
    [Output('graph-content', 'figure'),
     Output('info-content', 'children')],
    Input('dropdown-selection', 'value')
)
def update_graph(selected_ticker_input):
    global selected_ticker

    try:
        if selected_ticker_input is None:
            return go.Figure(), None

        selected_ticker = selected_ticker_input

        data = yf.download(selected_ticker, '2023-01-01', datetime.now())
        
        df = pd.DataFrame(data, columns=['Open', 'High', 'Low', 'Close'])

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

        # Adicione informações adicionais que você deseja exibir
        info_content = f""

        return fig, info_content

    except Exception as e:
        error_message = f"Error: {e}"
        return go.Figure(), error_message

if __name__ == '__main__':
    app.run_server(debug=True)