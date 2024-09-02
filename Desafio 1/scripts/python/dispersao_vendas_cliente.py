import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Diretórios
data_dir = os.path.join('..', '..', 'arquivos')
graphics_dir = os.path.join('..', '..', 'Graficos')

def read_csv_with_encoding(filepath):
    """Tenta ler um CSV com diferentes encodings."""
    encodings = ['utf-8', 'latin1', 'cp1252']
    for encoding in encodings:
        try:
            return pd.read_csv(filepath, encoding=encoding)
        except (UnicodeDecodeError, pd.errors.ParserError):
            continue
    raise ValueError("Não foi possível ler o arquivo com os encodings testados.")

# Carregar dados com tratamento de encoding
customers = read_csv_with_encoding(os.path.join(data_dir, 'AdventureWorks_Customers.csv'))
sales_2015 = pd.read_csv(os.path.join(data_dir, 'AdventureWorks_Sales_2015.csv'))
sales_2016 = pd.read_csv(os.path.join(data_dir, 'AdventureWorks_Sales_2016.csv'))
sales_2017 = pd.read_csv(os.path.join(data_dir, 'AdventureWorks_Sales_2017.csv'))
products = pd.read_csv(os.path.join(data_dir, 'AdventureWorks_Products.csv'))

# Filtrar dados e unir
sales = pd.concat([sales_2015, sales_2016, sales_2017])
sales = sales.merge(products[['ProductKey', 'ProductPrice']], on='ProductKey')
sales['TotalSales'] = sales['OrderQuantity'] * sales['ProductPrice']
sales_grouped = sales.groupby('CustomerKey').agg({'TotalSales': 'sum', 'OrderQuantity': 'sum'}).reset_index()

# Plotar
plt.figure(figsize=(12, 8))
sns.scatterplot(data=sales_grouped, x='OrderQuantity', y='TotalSales', alpha=0.7)
sns.regplot(data=sales_grouped, x='OrderQuantity', y='TotalSales', scatter=False, color='red')
plt.xlabel('Número de Vendas')
plt.ylabel('Valor Total das Vendas')
plt.title('Relação entre Número de Vendas e Valor Total por Cliente')
plt.tight_layout()
plt.savefig(os.path.join(graphics_dir, 'dispersao_vendas_cliente.png'))
plt.show()
