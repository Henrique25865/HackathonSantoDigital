import 'dart:io';
import 'package:sqlite3/sqlite3.dart';

void main() {
  // Conecte-se ao banco de dados
  final Database db = sqlite3.open('${Directory.current.path}/db/AdventureWorksDataBase.sqlite');

  try {
    // Consulta para obter os territórios com vendas acima da média e crescimento superior a 10%
    final ResultSet result = db.select('''
      WITH Sales2017 AS (
        SELECT
            TerritoryKey,
            SUM(OrderQuantity * p.ProductPrice) AS TotalSales2017
        FROM
            Sales_2017 s
            JOIN Products p ON s.ProductKey = p.ProductKey
        GROUP BY
            s.TerritoryKey
      ),
      Sales2016 AS (
        SELECT
            TerritoryKey,
            SUM(OrderQuantity * p.ProductPrice) AS TotalSales2016
        FROM
            Sales_2016 s
            JOIN Products p ON s.ProductKey = p.ProductKey
        GROUP BY
            s.TerritoryKey
      ),
      AverageSales2017 AS (
        SELECT AVG(TotalSales2017) AS AvgSales2017 FROM Sales2017
      ),
      SellersAboveAverage AS (
        SELECT
            s2017.TerritoryKey,
            s2017.TotalSales2017,
            s2016.TotalSales2016,
            (s2017.TotalSales2017 - s2016.TotalSales2016) / s2016.TotalSales2016 * 100 AS GrowthRate
        FROM
            Sales2017 s2017
            JOIN Sales2016 s2016 ON s2017.TerritoryKey = s2016.TerritoryKey
            CROSS JOIN AverageSales2017 avg
        WHERE
            s2017.TotalSales2017 > avg.AvgSales2017
      )
      SELECT
        s.TerritoryKey,
        t.Region,
        t.Country,
        s.TotalSales2017,
        s.TotalSales2016,
        s.GrowthRate
      FROM
        SellersAboveAverage s
        JOIN Territories t ON s.TerritoryKey = t.SalesTerritoryKey
      WHERE
        s.GrowthRate > 10
      ORDER BY
        s.GrowthRate DESC;
    ''');

    // Verificar se houve resultados e imprimir a saída formatada
    if (result.isEmpty) {
      print('Nenhum vendedor atendeu aos critérios.');
    } else {
      print('Vendedores com crescimento de vendas superior a 10% e vendas acima da média em 2017:');
      for (final row in result) {
        final int territoryKey = row['TerritoryKey'] as int;
        final String region = row['Region'] as String;
        final String country = row['Country'] as String;
        final double totalSales2017 = row['TotalSales2017'] as double;
        final double totalSales2016 = row['TotalSales2016'] as double;
        final double growthRate = row['GrowthRate'] as double;

        print('Território: $territoryKey');
        print('Região: $region');
        print('País: $country');
        print('Vendas em 2017: \$${totalSales2017.toStringAsFixed(2)}');
        print('Vendas em 2016: \$${totalSales2016.toStringAsFixed(2)}');
        print('Taxa de Crescimento: ${growthRate.toStringAsFixed(2)}% \n');
      }
    }
  } on SqliteException catch (e) {
    print('Erro ao executar a consulta: ${e.message}');
  } finally {
    db.dispose();
  }
}
