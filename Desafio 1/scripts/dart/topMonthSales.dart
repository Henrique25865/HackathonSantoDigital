import 'dart:io';
import 'package:sqlite3/sqlite3.dart';

void main() {
  // Conecte-se ao banco de dados
  final Database db = sqlite3.open('${Directory.current.path}/db/AdventureWorksDataBase.sqlite');

  // Consulta SQL para calcular a receita total e a receita média por mês
  final result = db.select('''
    WITH MonthlySales AS (
      SELECT 
        strftime('%m', OrderDate) AS Month,
        SUM(OrderQuantity * p.ProductPrice) AS TotalRevenue,
        AVG(OrderQuantity * p.ProductPrice) AS AverageRevenuePerSale
      FROM 
        Sales_2016 s
        JOIN Products p ON s.ProductKey = p.ProductKey
      GROUP BY 
        strftime('%m', OrderDate)
      HAVING 
        AVG(OrderQuantity * p.ProductPrice) > 500
    UNION ALL
      SELECT 
        strftime('%m', OrderDate) AS Month,
        SUM(OrderQuantity * p.ProductPrice) AS TotalRevenue,
        AVG(OrderQuantity * p.ProductPrice) AS AverageRevenuePerSale
      FROM 
        Sales_2017 s
        JOIN Products p ON s.ProductKey = p.ProductKey
      GROUP BY 
        strftime('%m', OrderDate)
      HAVING 
        AVG(OrderQuantity * p.ProductPrice) > 500
    )
    SELECT 
      Month, 
      SUM(TotalRevenue) AS TotalRevenue
    FROM 
      MonthlySales
    GROUP BY 
      Month
    ORDER BY 
      TotalRevenue DESC
    LIMIT 1;
  ''');

  // Verifica se há resultados e imprime o mês com mais vendas
  if (result.isNotEmpty) {
    final row = result.first;
    print('Mês com mais vendas (superior a 500 unidades monetárias): ${row['Month']}');
    print('Receita total: ${row['TotalRevenue']} unidades monetárias');
  } else {
    print('Nenhum mês atendeu aos critérios.');
  }

  // Fecha a conexão com o banco de dados
  db.dispose();
}
