import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Diretórios
data_dir = os.path.join('..', '..', 'arquivos')
graphics_dir = os.path.join('..', '..', 'Graficos')

# Carregar dados
sales_2015 = pd.read_csv(os.path.join(data_dir, 'AdventureWorks_Sales_2015.csv'))
sales_2016 = pd.read_csv(os.path.join(data_dir, 'AdventureWorks_Sales_2016.csv'))
sales_2017 = pd.read_csv(os.path.join(data_dir, 'AdventureWorks_Sales_2017.csv'))
territories = pd.read_csv(os.path.join(data_dir, 'AdventureWorks_Territories.csv'))

# Filtrar dados e unir
sales = pd.concat([sales_2015, sales_2016, sales_2017])
sales['OrderDate'] = pd.to_datetime(sales['OrderDate'])
sales['MonthYear'] = sales['OrderDate'].dt.to_period('M')

sales = sales.merge(territories, left_on='TerritoryKey', right_on='SalesTerritoryKey')
sales_grouped = sales.groupby(['Region', 'MonthYear']).agg({'OrderQuantity': 'sum'}).reset_index()

# Pivotar para mapa de calor
heatmap_data = sales_grouped.pivot(index='Region', columns='MonthYear', values='OrderQuantity')

# Plotar
plt.figure(figsize=(14, 8))
sns.heatmap(heatmap_data, cmap='YlGnBu', annot=True, fmt='g')
plt.title('Mapa de Calor das Vendas por Região e por Mês')
plt.tight_layout()
plt.savefig(os.path.join(graphics_dir, 'mapa_calor_vendas_regiao_mes.png'))
plt.show()
