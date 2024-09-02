import pandas as pd
import matplotlib.pyplot as plt
import os

# Diretórios
data_dir = os.path.join('..', '..', 'arquivos')
graphics_dir = os.path.join('..', '..', 'Graficos')

# Carregar dados
sales_2016 = pd.read_csv(os.path.join(data_dir, 'AdventureWorks_Sales_2016.csv'))
sales_2017 = pd.read_csv(os.path.join(data_dir, 'AdventureWorks_Sales_2017.csv'))

# Converter OrderDate para datetime
sales_2016['OrderDate'] = pd.to_datetime(sales_2016['OrderDate'])
sales_2017['OrderDate'] = pd.to_datetime(sales_2017['OrderDate'])

# Agrupar por mês e ano e somar vendas
sales_2016['MonthYear'] = sales_2016['OrderDate'].dt.to_period('M')
sales_2017['MonthYear'] = sales_2017['OrderDate'].dt.to_period('M')

sales_2016_monthly = sales_2016.groupby('MonthYear').size()
sales_2017_monthly = sales_2017.groupby('MonthYear').size()

# Plotar
plt.figure(figsize=(12, 6))
plt.bar(sales_2016_monthly.index.astype(str), sales_2016_monthly, label='2016', color='lightblue', alpha=0.6)
plt.bar(sales_2017_monthly.index.astype(str), sales_2017_monthly, label='2017', color='salmon', alpha=0.6)
plt.xlabel('Data')
plt.ylabel('Total de Vendas')
plt.title('Comparação de Vendas Mensais entre 2016 e 2017')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(graphics_dir, 'comparacao_vendas_mensais_2016_2017.png'))
plt.show()
