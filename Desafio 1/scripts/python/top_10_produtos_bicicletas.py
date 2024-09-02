import pandas as pd
import matplotlib.pyplot as plt
import os

# Diretórios
data_dir = os.path.join('..', '..', 'arquivos')
graphics_dir = os.path.join('..', '..', 'Graficos')

# Criar diretório para gráficos se não existir
os.makedirs(graphics_dir, exist_ok=True)

# Carregar dados
sales_2015 = pd.read_csv(os.path.join(data_dir, 'AdventureWorks_Sales_2015.csv'))
sales_2016 = pd.read_csv(os.path.join(data_dir, 'AdventureWorks_Sales_2016.csv'))
sales_2017 = pd.read_csv(os.path.join(data_dir, 'AdventureWorks_Sales_2017.csv'))
products = pd.read_csv(os.path.join(data_dir, 'AdventureWorks_Products.csv'))
categories = pd.read_csv(os.path.join(data_dir, 'AdventureWorks_Product_Categories.csv'))
subcategories = pd.read_csv(os.path.join(data_dir, 'AdventureWorks_Product_Subcategories.csv'))

# Filtrar dados da categoria "Bikes"
bikes_subcategories = subcategories[subcategories['ProductCategoryKey'] == 1]
bikes_products = products[products['ProductSubcategoryKey'].isin(bikes_subcategories['ProductSubcategoryKey'])]
sales = pd.concat([sales_2015, sales_2016, sales_2017])

# Juntar dados
sales = sales.merge(bikes_products[['ProductKey', 'ProductName', 'ProductPrice']], on='ProductKey')
sales_grouped = sales.groupby('ProductName').agg({'OrderQuantity': 'sum', 'ProductPrice': 'sum'}).reset_index()
sales_grouped['TotalSales'] = sales_grouped['OrderQuantity'] * sales_grouped['ProductPrice']
top_10_products = sales_grouped.nlargest(10, 'TotalSales')

# Plotar
plt.figure(figsize=(12, 8))
plt.barh(top_10_products['ProductName'], top_10_products['TotalSales'], color='skyblue')
plt.xlabel('Vendas Totais (em unidades monetárias)')
plt.title('Top 10 Produtos Mais Vendidos na Categoria "Bicicletas"')
plt.tight_layout()
plt.savefig(os.path.join(graphics_dir, 'top_10_produtos_bicicletas.png'))
plt.close()
