import sqlite3
import pandas as pd
import os

def create_database_from_schema(schema_file, db_file):
    """Cria o banco de dados e as tabelas a partir do arquivo de esquema."""
    with open(schema_file, 'r') as f:
        schema_sql = f.read()
    
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Executa o script do esquema para criar tabelas se não existirem
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS Calendar (
        Date TEXT PRIMARY KEY
    );
    CREATE TABLE IF NOT EXISTS Customers (
        CustomerKey INTEGER PRIMARY KEY,
        Prefix TEXT,
        FirstName TEXT,
        LastName TEXT,
        BirthDate TEXT,
        MaritalStatus TEXT,
        Gender TEXT,
        EmailAddress TEXT,
        AnnualIncome REAL,
        TotalChildren INTEGER,
        EducationLevel TEXT,
        Occupation TEXT,
        HomeOwner TEXT
    );
    CREATE TABLE IF NOT EXISTS ProductCategories (
        ProductCategoryKey INTEGER PRIMARY KEY,
        CategoryName TEXT
    );
    CREATE TABLE IF NOT EXISTS ProductSubcategories (
        ProductSubcategoryKey INTEGER PRIMARY KEY,
        SubcategoryName TEXT,
        ProductCategoryKey INTEGER,
        FOREIGN KEY (ProductCategoryKey) REFERENCES ProductCategories(ProductCategoryKey)
    );
    CREATE TABLE IF NOT EXISTS Products (
        ProductKey INTEGER PRIMARY KEY,
        ProductSubcategoryKey INTEGER,
        ProductSKU TEXT,
        ProductName TEXT,
        ModelName TEXT,
        ProductDescription TEXT,
        ProductColor TEXT,
        ProductSize TEXT,
        ProductStyle TEXT,
        ProductCost REAL,
        ProductPrice REAL,
        FOREIGN KEY (ProductSubcategoryKey) REFERENCES ProductSubcategories(ProductSubcategoryKey)
    );
    CREATE TABLE IF NOT EXISTS Returns (
        ReturnDate TEXT,
        TerritoryKey INTEGER,
        ProductKey INTEGER,
        ReturnQuantity INTEGER,
        FOREIGN KEY (ProductKey) REFERENCES Products(ProductKey)
    );
    CREATE TABLE IF NOT EXISTS Sales_2015 (
        OrderDate TEXT,
        StockDate TEXT,
        OrderNumber TEXT,
        ProductKey INTEGER,
        CustomerKey INTEGER,
        TerritoryKey INTEGER,
        OrderLineItem INTEGER,
        OrderQuantity INTEGER,
        FOREIGN KEY (ProductKey) REFERENCES Products(ProductKey),
        FOREIGN KEY (CustomerKey) REFERENCES Customers(CustomerKey)
    );
    CREATE TABLE IF NOT EXISTS Sales_2016 (
        OrderDate TEXT,
        StockDate TEXT,
        OrderNumber TEXT,
        ProductKey INTEGER,
        CustomerKey INTEGER,
        TerritoryKey INTEGER,
        OrderLineItem INTEGER,
        OrderQuantity INTEGER,
        FOREIGN KEY (ProductKey) REFERENCES Products(ProductKey),
        FOREIGN KEY (CustomerKey) REFERENCES Customers(CustomerKey)
    );
    CREATE TABLE IF NOT EXISTS Sales_2017 (
        OrderDate TEXT,
        StockDate TEXT,
        OrderNumber TEXT,
        ProductKey INTEGER,
        CustomerKey INTEGER,
        TerritoryKey INTEGER,
        OrderLineItem INTEGER,
        OrderQuantity INTEGER,
        FOREIGN KEY (ProductKey) REFERENCES Products(ProductKey),
        FOREIGN KEY (CustomerKey) REFERENCES Customers(CustomerKey)
    );
    CREATE TABLE IF NOT EXISTS Territories (
        SalesTerritoryKey INTEGER PRIMARY KEY,
        Region TEXT,
        Country TEXT,
        Continent TEXT
    );
    """)
    conn.commit()
    conn.close()

def fill_table_from_csv(csv_file, db_file, table_name):
    """Preenche a tabela do banco de dados a partir de um arquivo CSV."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Tenta ler o CSV usando pandas com diferentes codificações
    try:
        df = pd.read_csv(csv_file, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(csv_file, encoding='ISO-8859-1')
    
    # Construa a instrução SQL para inserir os dados
    columns = ', '.join(df.columns)
    placeholders = ', '.join('?' * len(df.columns))
    insert_sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    
    # Insere os dados na tabela
    cursor.executemany(insert_sql, df.values.tolist())
    conn.commit()
    conn.close()

def transfer_data(db_file, table_mappings):
    """Transfere dados das tabelas AdventureWorks_* para as tabelas correspondentes."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    for source_table, target_table in table_mappings.items():
        print(f"Transferring data from {source_table} to {target_table}...")
        try:
            # Verifica se a tabela fonte existe
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{source_table}'")
            if cursor.fetchone() is None:
                print(f"Table {source_table} does not exist.")
                continue
            
            # Cria uma tabela temporária
            cursor.execute(f"CREATE TABLE IF NOT EXISTS temp AS SELECT * FROM {source_table} WHERE 0")
            # Copia os dados para a tabela temporária
            cursor.execute(f"INSERT INTO temp SELECT * FROM {source_table}")
            # Apaga os dados da tabela alvo e insere dados da tabela temporária
            cursor.execute(f"DELETE FROM {target_table}")
            cursor.execute(f"INSERT INTO {target_table} SELECT * FROM temp")
            # Remove a tabela temporária
            cursor.execute("DROP TABLE temp")
            conn.commit()
            print(f"Data transferred from {source_table} to {target_table}")
        except sqlite3.Error as e:
            print(f"An error occurred during data transfer: {e}")
    
    conn.close()

def drop_old_tables(db_file, old_tables):
    """Remove as tabelas antigas AdventureWorks_* do banco de dados."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    for table in old_tables:
        try:
            cursor.execute(f"DROP TABLE IF EXISTS {table}")
            conn.commit()
            print(f"Table {table} dropped")
        except sqlite3.Error as e:
            print(f"An error occurred while dropping table {table}: {e}")
    
    conn.close()

def main():
    # Caminhos dos arquivos
    script_dir = os.path.dirname(os.path.abspath(__file__))
    schema_file = os.path.join(script_dir, '../../scripts/sql/schema.sql')
    db_file = os.path.join(script_dir, '../../db/AdventureWorksDataBase.sqlite')
    
    # Criação do banco de dados e tabelas
    print("Creating database and tables from schema...")
    create_database_from_schema(schema_file, db_file)
    
    # Caminho para os arquivos CSV
    csv_dir = os.path.join(script_dir, '../../arquivos')
    
    # Mapeamento das tabelas
    table_mappings = {
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
    
    # Preenchendo as tabelas com dados dos arquivos CSV
    for csv_name, table_name in table_mappings.items():
        csv_file = os.path.join(csv_dir, f"{csv_name}.csv")
        print(f"Reading data from: {csv_file}")
        try:
            fill_table_from_csv(csv_file, db_file, table_name)
        except Exception as e:
            print(f"An error occurred: {e}")
    
    # Transferindo dados das tabelas AdventureWorks_* para as tabelas correspondentes
    transfer_data(db_file, table_mappings)
    
    # Dropar as tabelas antigas AdventureWorks_*
    old_tables = list(table_mappings.keys())
    drop_old_tables(db_file, old_tables)

if __name__ == '__main__':
    main()
