import 'package:sqlite3/sqlite3.dart';

void main() {
  // Caminho para o arquivo do banco de dados
  final dbPath = '../../db/AdventureWorksDataBase.sqlite';
  
  // Abrindo a conexão com o banco de dados
  final database = sqlite3.open(dbPath);

  // Consultando os 10 produtos mais vendidos na categoria 'Bicicletas' para os anos de 2016 e 2017
  final query = '''
    -- Primeiro, vamos identificar o ProductCategoryKey para a categoria 'Bikes'
    WITH CategoryKeys AS (
        SELECT ProductCategoryKey
        FROM ProductCategories
        WHERE CategoryName = 'Bikes'
    ),
    -- Agora, encontramos os ProductSubcategoryKeys associados a esta categoria
    SubcategoryKeys AS (
        SELECT ProductSubcategoryKey
        FROM ProductSubcategories
        WHERE ProductCategoryKey IN (SELECT ProductCategoryKey FROM CategoryKeys)
    ),
    -- Obtemos a lista dos produtos na(s) subcategoria(s) identificada(s)
    ProductsInCategory AS (
        SELECT ProductKey
        FROM Products
        WHERE ProductSubcategoryKey IN (SELECT ProductSubcategoryKey FROM SubcategoryKeys)
    ),
    -- Somamos as quantidades vendidas para os produtos da categoria nos anos de 2016 e 2017
    SalesSummary AS (
        SELECT ProductKey, SUM(OrderQuantity) AS TotalQuantity
        FROM (
            SELECT ProductKey, OrderQuantity FROM Sales_2016
            UNION ALL
            SELECT ProductKey, OrderQuantity FROM Sales_2017
        )
        WHERE ProductKey IN (SELECT ProductKey FROM ProductsInCategory)
        GROUP BY ProductKey
    )
    -- Finalmente, obtemos os 10 produtos mais vendidos
    SELECT p.ProductName, ss.TotalQuantity
    FROM SalesSummary ss
    JOIN Products p ON ss.ProductKey = p.ProductKey
    ORDER BY ss.TotalQuantity DESC
    LIMIT 10;
  ''';

  final result = database.select(query);

  // Fechando a conexão com o banco de dados
  database.dispose();

  // Exibindo os resultados
  print('Top 10 Produtos Mais Vendidos na Categoria "Bicicletas":');
  for (var row in result) {
    print('${row['ProductName']}: ${row['TotalQuantity']}');
  }
}



