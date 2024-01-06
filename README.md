O dashboard só possui duas seções - cotações e notícias. A duas seções são diretamente ligadas ao dropdown que escolhe uma das 3 ações disponíveis: CEAB3, WEGE3 e PETR4. Ao trocar a empresa, o gráfico de candle e as notícias são atualizadas.
 
As notícias foram coletadas no Brazil Journal. Basta utilizar a lupa da página principal para pesquisar as últimas notícias de um ticker, chegando em um link como esse: https://braziljournal.com/?s=petr4. A partir disso, você pode fazer o scraping pra coletar as informações necessárias.
 
Dessa forma, a coleta de dados terá duas fontes: o jornal e uma fonte de cotações a sua escolha. A forma de armazenamento desses dados e como eles irão se conectar ao seu dashboard ficará ao seu critério.
 
O dashboard do link disponível foi construído utilizando dash + plotly. O ideal é usar esse mesmo framework. É importante destacar que ali também possuí uma leve camada de CSS, mas isso não será avaliado na tarefa. Sem css é impossível criar algo bonito com dashboards, mas o objetivo aqui é avaliar a forma que você irá estruturar a coleta, 
armazenamento e visualização dos dados. Essa estilização final é mero detalhe, o importante é que o seu projeto tenha as mesmas funcionalidades do meu, então mexa no meu dash para se certificar que no seu não esteja faltando nada.
