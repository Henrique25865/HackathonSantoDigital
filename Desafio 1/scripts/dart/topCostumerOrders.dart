import 'package:sqlite3/sqlite3.dart';

void main() {
  final db = sqlite3.open('../../db/AdventureWorksDataBase.sqlite');

  // Definir os trimestres
  const trimesters = {
    'Q1': ['01/01', '03/31'],
    'Q2': ['04/01', '06/30'],
    'Q3': ['07/01', '09/30'],
    'Q4': ['10/01', '12/31']
  };

  // Consultar clientes que fizeram pedidos em cada trimestre
  final customersPerQuarter = <String, Set<int>>{};
  for (var quarter in trimesters.keys) {
    final startDate = trimesters[quarter]![0];
    final endDate = trimesters[quarter]![1];

    final query = '''
      SELECT CustomerKey
      FROM Sales_2017
      WHERE OrderDate BETWEEN '$startDate/2017' AND '$endDate/2017'
    ''';

    final result = db.select(query);

    final customerKeys = result.map((row) => row['CustomerKey'] as int).toSet();
    customersPerQuarter[quarter] = customerKeys;
  }

  // Encontrar clientes que fizeram pedidos em todos os trimestres
  final customersInAllQuarters = customersPerQuarter.values.reduce((a, b) => a.intersection(b));

  if (customersInAllQuarters.isEmpty) {
    print('Nenhum cliente atendeu aos critérios.');
    db.dispose();
    return;
  }

  // Contar o número total de pedidos desses clientes
  final customerOrderCount = <int, int>{};
  for (var customerKey in customersInAllQuarters) {
    final query = '''
      SELECT COUNT(*) as OrderCount
      FROM Sales_2017
      WHERE CustomerKey = $customerKey
    ''';

    final result = db.select(query);
    customerOrderCount[customerKey] = result.first['OrderCount'] as int;
  }

  // Encontrar o cliente com o maior número de pedidos
  final topCustomer = customerOrderCount.entries.reduce((a, b) => a.value > b.value ? a : b);

  // Recuperar os dados do cliente
  final customerData = db.select('''
    SELECT *
    FROM Customers
    WHERE CustomerKey = ${topCustomer.key}
  ''');

  if (customerData.isNotEmpty) {
    print('Cliente com maior número de pedidos:');
    print('Nome: ${customerData.first['FirstName']} ${customerData.first['LastName']}');
    print('Email: ${customerData.first['EmailAddress']}');
    print('Total de pedidos: ${topCustomer.value}');
  } else {
    print('Nenhum cliente encontrado.');
  }

  db.dispose();
}
