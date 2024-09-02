import sqlite3

# Caminho para o banco de dados
db_file = '../../db/AdventureWorksDataBase.sqlite'

# Mapeamento das tabelas de origem e destino
table_mapping = {
    'AdventureWorks_Calendar': 'Calendar',
    'AdventureWorks_Customers': 'Customers',
    'AdventureWorks_Product_Categories': 'ProductCategories',
    'AdventureWorks_Product_Subcategories': 'ProductSubcategories',
    'AdventureWorks_Products': 'Products',
    'AdventureWorks_Returns': 'Returns',
    'AdventureWorks_Sales_2015': 'Sales_2015',
    'AdventureWorks_Sales_2016': 'Sales_2016',
    'AdventureWorks_Sales_2017': 'Sales_2017',
    'AdventureWorks_Territories': 'Territories'
}

# Função para transferir dados entre tabelas
def transfer_data(source_table, dest_table, conn):
    try:
        # Criar um cursor para executar comandos SQL
        cursor = conn.cursor()
        
        # Ler dados da tabela de origem
        cursor.execute(f"SELECT * FROM {source_table}")
        rows = cursor.fetchall()
        
        # Inserir dados na tabela de destino
        columns = [desc[0] for desc in cursor.description]
        columns_str = ', '.join(columns)
        placeholders = ', '.join('?' * len(columns))
        
        insert_query = f"INSERT INTO {dest_table} ({columns_str}) VALUES ({placeholders})"
        
        cursor.executemany(insert_query, rows)
        
        # Confirmar as alterações
        conn.commit()
        print(f"Dados da tabela {source_table} transferidos para a tabela {dest_table} com sucesso.")
        
    except sqlite3.Error as e:
        print(f"Erro ao transferir dados da tabela {source_table} para {dest_table}: {e}")

# Conectar ao banco de dados
conn = sqlite3.connect(db_file)

# Transferir dados para cada tabela
for source_table, dest_table in table_mapping.items():
    transfer_data(source_table, dest_table, conn)

# Fechar a conexão
conn.close()

print("Transferência de dados concluída com sucesso.")
