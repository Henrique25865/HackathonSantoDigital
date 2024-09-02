import pandas as pd
import matplotlib.pyplot as plt
import os

# Definir o diretório de dados e o diretório para salvar os gráficos
data_dir = os.path.join('..', '..', 'arquivos')
graphics_dir = os.path.join('..', '..', 'Graficos')

# Criar o diretório para gráficos se não existir
os.makedirs(graphics_dir, exist_ok=True)

# Carregar dados
sales_2015 = pd.read_csv(os.path.join(data_dir, 'AdventureWorks_Sales_2015.csv'))
sales_2016 = pd.read_csv(os.path.join(data_dir, 'AdventureWorks_Sales_2016.csv'))
sales_2017 = pd.read_csv(os.path.join(data_dir, 'AdventureWorks_Sales_2017.csv'))

# Converter OrderDate para datetime
sales_2015['OrderDate'] = pd.to_datetime(sales_2015['OrderDate'])
sales_2016['OrderDate'] = pd.to_datetime(sales_2016['OrderDate'])
sales_2017['OrderDate'] = pd.to_datetime(sales_2017['OrderDate'])

# Agrupar por mês e ano e somar vendas
sales_2015['MonthYear'] = sales_2015['OrderDate'].dt.to_period('M')
sales_2016['MonthYear'] = sales_2016['OrderDate'].dt.to_period('M')
sales_2017['MonthYear'] = sales_2017['OrderDate'].dt.to_period('M')

sales_2015_monthly = sales_2015.groupby('MonthYear').size()
sales_2016_monthly = sales_2016.groupby('MonthYear').size()
sales_2017_monthly = sales_2017.groupby('MonthYear').size()

# Plotar
plt.figure(figsize=(12, 6))
plt.plot(sales_2015_monthly.index.astype(str), sales_2015_monthly, label='2015')
plt.plot(sales_2016_monthly.index.astype(str), sales_2016_monthly, label='2016')
plt.plot(sales_2017_monthly.index.astype(str), sales_2017_monthly, label='2017')
plt.xlabel('Data')
plt.ylabel('Total de Vendas')
plt.title('Tendência das Vendas Totais ao Longo do Tempo')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Salvar o gráfico
plt.savefig(os.path.join(graphics_dir, 'vendas_totais_tempo.png'))
plt.close()
